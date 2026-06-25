import json

from django.conf import settings
from django.db.models import Q
from openai import OpenAI, OpenAIError

from .models import DiagnosisResult, FinancialGuide


AREA_KEYWORDS = {
    '저축': ['저축', '자동이체', '월급', '목돈', '단기 목표'],
    '소비': ['소비', '고정비', '구독', '지출', '예산'],
    '투자': ['투자', '예적금', 'CMA', 'ISA', '위험'],
    '안정성': ['안정성', '비상금', '생활비', '현금흐름', '원금 손실'],
}

DEFAULT_GUIDES = [
    {
        'category': '사회초년생',
        'title': '기본 현금흐름 관리',
        'content': '사회초년생은 수익률보다 현금흐름 관리와 비상금 확보를 우선하는 것이 좋다.',
    }
]


def _score_value(value):
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        filled = value.count('★')
        if filled:
            return filled * 20
        try:
            return int(value)
        except ValueError:
            return 0
    return 0


def _raw_score(raw_scores, names):
    for name in names:
        if name in raw_scores:
            return _score_value(raw_scores.get(name))
    return 0


def get_diagnosis_area_scores(diagnosis):
    raw_scores = diagnosis.profile_scores or {}
    spending = _raw_score(raw_scores, ['소비 관리', '소비'])
    investment = _raw_score(raw_scores, ['투자 성향', '투자'])
    saving = _raw_score(raw_scores, ['저축 습관', '저축'])
    stability = _raw_score(raw_scores, ['자산 관리', '안정성'])

    if not any([saving, spending, investment, stability]):
        total = int(diagnosis.readiness_score or 0)
        saving = spending = investment = stability = total

    return {
        '저축': saving,
        '소비': spending,
        '투자': investment,
        '안정성': stability,
    }


def get_weak_areas(diagnosis, limit=2):
    scores = get_diagnosis_area_scores(diagnosis)
    weak = [item for item in sorted(scores.items(), key=lambda item: item[1]) if item[1] < 70]
    if not weak:
        weak = sorted(scores.items(), key=lambda item: item[1])[:1]
    return [area for area, _ in weak[:limit]]


def get_strong_areas(diagnosis, limit=2):
    scores = get_diagnosis_area_scores(diagnosis)
    strong = [item for item in sorted(scores.items(), key=lambda item: item[1], reverse=True) if item[1] >= 70]
    if not strong:
        strong = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:1]
    return [area for area, _ in strong[:limit]]


def search_financial_guides(areas=None, keywords=None, limit=5):
    areas = areas or []
    keywords = keywords or []
    terms = set(areas)
    for area in areas:
        terms.update(AREA_KEYWORDS.get(area, []))
    terms.update(keywords)

    query = Q()
    for term in terms:
        if term:
            query |= Q(category__icontains=term) | Q(keywords__icontains=term) | Q(title__icontains=term)

    if not query:
        query = Q(category__in=['사회초년생', '비상금'])

    guides = list(FinancialGuide.objects.filter(query).distinct()[:limit])
    if not guides:
        return DEFAULT_GUIDES
    return [
        {
            'id': guide.id,
            'category': guide.category,
            'title': guide.title,
            'content': guide.content,
        }
        for guide in guides
    ]


def format_guides_for_prompt(guides):
    if not guides:
        return '참고 가능한 금융 가이드가 없습니다.'
    return '\n'.join(
        f"- [{guide.get('category')}] {guide.get('title')}: {guide.get('content')}"
        for guide in guides
    )


def diagnosis_context(diagnosis):
    area_scores = get_diagnosis_area_scores(diagnosis)
    return {
        'financial_type': diagnosis.financial_type or diagnosis.level,
        'readiness_score': diagnosis.readiness_score,
        'income_level': diagnosis.income_level,
        'spending_style': diagnosis.spending_style,
        'financial_goal': diagnosis.financial_goal,
        'investment_style': diagnosis.investment_style,
        'asset_level': diagnosis.asset_level,
        'loan_type': diagnosis.loan_type,
        'area_scores': area_scores,
        'strong_areas': get_strong_areas(diagnosis),
        'weak_areas': get_weak_areas(diagnosis),
    }


def call_json_ai(prompt, fallback):
    if not settings.GMS_API_KEY or not settings.GMS_OPENAI_BASE_URL:
        return fallback

    client = OpenAI(api_key=settings.GMS_API_KEY, base_url=settings.GMS_OPENAI_BASE_URL)
    try:
        response = client.chat.completions.create(
            model=settings.GMS_OPENAI_MODEL,
            messages=[
                {'role': 'system', 'content': '당신은 사회초년생을 위한 금융 코치입니다. 반드시 입력된 진단 결과와 참고자료에 근거해 답변합니다.'},
                {'role': 'user', 'content': prompt},
            ],
            temperature=0.25,
            response_format={'type': 'json_object'},
        )
        return json.loads(response.choices[0].message.content or '{}')
    except (OpenAIError, json.JSONDecodeError, TypeError, ValueError):
        return fallback


def normalize_list(value, fallback, limit=2):
    items = value if isinstance(value, list) else []
    cleaned = []
    for item in items + fallback:
        text = ' '.join(str(item).split())
        if text and text not in cleaned:
            cleaned.append(text)
        if len(cleaned) >= limit:
            break
    return cleaned


def fallback_strengths_for_diagnosis(diagnosis):
    scores = get_diagnosis_area_scores(diagnosis)
    context = diagnosis_context(diagnosis)
    strengths = []

    if scores['투자'] >= 90:
        strengths.append("투자 성향이 뚜렷해 상품의 수익과 위험을 함께 살펴볼 준비가 되어 있어요.")
    elif scores['투자'] >= 70:
        strengths.append("투자 위험을 인식하고 금융상품을 비교해볼 준비가 되어 있어요.")

    if scores['저축'] >= 70:
        strengths.append(f"{context['financial_goal']} 목표를 위해 저축 계획을 세울 기반이 있어요.")
    if scores['소비'] >= 70:
        strengths.append("소비를 조절하려는 기준이 있어 목표 자금으로 돌릴 여력이 보여요.")
    if scores['안정성'] >= 70:
        strengths.append("자산과 부채 상태를 점검하며 안정성을 관리할 기반이 있어요.")

    if not strengths:
        strengths.append("진단을 통해 현재 금융 상태를 점검하고 개선 방향을 찾기 시작했어요.")
    return strengths[:2]


def fallback_weaknesses_for_diagnosis(diagnosis):
    scores = get_diagnosis_area_scores(diagnosis)
    context = diagnosis_context(diagnosis)
    weaknesses = []

    if scores['소비'] < 70:
        weaknesses.append("고정비와 구독 지출을 먼저 정리하면 저축 여력을 더 만들 수 있어요.")
    if scores['저축'] < 70:
        weaknesses.append("월급일 다음 날 자동이체를 걸어 저축을 먼저 떼어두는 습관이 필요해요.")
    if scores['안정성'] < 70:
        weaknesses.append("단기 목표 자금과 비상금은 원금 손실 가능성이 낮은 상품부터 고려해보세요.")
    if scores['투자'] < 70:
        weaknesses.append("고위험 상품보다 예적금, CMA, ISA 같은 기초 상품부터 이해하면 좋아요.")

    if not weaknesses:
        weaknesses.append("공격형 투자 성향일수록 단기 목표 자금은 안전한 상품과 분리해두세요.")
        weaknesses.append(f"{context['financial_goal']} 목표에 맞춰 비상금과 투자금을 따로 관리해보세요.")
    return weaknesses[:2]


def build_rag_diagnosis_insights(diagnosis, fallback_strengths, fallback_improvements):
    context = diagnosis_context(diagnosis)
    guide_areas = list(dict.fromkeys(context['weak_areas'] + context['strong_areas']))
    guides = search_financial_guides(guide_areas)
    fallback = {
        'strengths': fallback_strengths_for_diagnosis(diagnosis) or fallback_strengths,
        'weaknesses': fallback_weaknesses_for_diagnosis(diagnosis) or fallback_improvements,
        'today_message': '오늘은 지출을 한 번 점검하고 비상금 목표를 작게라도 세워보세요.',
        'recommendation_reason': '',
    }
    prompt = f"""
역할: 사회초년생을 위한 금융 코치

입력: 사용자의 금융진단 결과
{json.dumps(context, ensure_ascii=False)}

[참고 금융 가이드]
{format_guides_for_prompt(guides)}

작성 목표:
- 강점은 높은 점수 영역과 실제 답변을 연결해 구체적으로 칭찬합니다.
- 보완점은 낮은 점수 영역과 참고 금융 가이드의 행동 제안을 연결해 작성합니다.
- 단순한 말투(예: "좋은 흐름", "잘 갖춰져 있어요")만 반복하지 않습니다.
- 각 문장은 사용자가 바로 이해할 수 있는 45자 안팎의 한국어 문장으로 작성합니다.

제약조건:
- 과장된 투자 권유 금지
- 원금 손실 가능 상품에 대해 단정적으로 추천 금지
- 진단 결과와 참고자료에 근거해서 작성
- 없는 정보를 지어내지 않기
- strengths 2개, weaknesses 2개만 작성

출력 형식:
{{"strengths":["...","..."],"weaknesses":["...","..."],"today_message":"...","recommendation_reason":""}}
"""
    result = call_json_ai(prompt, fallback)
    return {
        'strengths': normalize_list(result.get('strengths'), fallback['strengths'], limit=2),
        'weaknesses': normalize_list(result.get('weaknesses') or result.get('improvements'), fallback['weaknesses'], limit=2),
        'today_message': str(result.get('today_message') or fallback['today_message']).strip(),
        'recommendation_reason': str(result.get('recommendation_reason') or '').strip(),
        'guides': guides,
    }


def build_today_message(user):
    diagnosis = DiagnosisResult.objects.filter(user=user).order_by('-created_at').first()
    if diagnosis:
        weak_areas = get_weak_areas(diagnosis, limit=1)
        context = diagnosis_context(diagnosis)
    else:
        weak_areas = ['사회초년생']
        context = {'message': '진단 결과 없음', 'target': '사회초년생 기본 금융 습관'}

    guides = search_financial_guides(weak_areas, limit=3)
    prompt = f"""
역할: 사회초년생을 위한 금융 코치

입력: {json.dumps(context, ensure_ascii=False)}

[참고 금융 가이드]
{format_guides_for_prompt(guides)}

제약조건:
- 과장된 투자 권유 금지
- 참고자료와 입력에 근거하기
- 1문장, 80자 이내로 작성
- 없는 정보를 지어내지 않기

출력 형식:
{{"today_message":"..."}}
"""
    fallback_message = '오늘은 고정비와 구독 서비스를 점검하고 남는 금액을 비상금으로 옮겨보세요.'
    result = call_json_ai(prompt, {'today_message': fallback_message})
    return {
        'message': str(result.get('today_message') or fallback_message).strip(),
        'guides': guides,
        'has_diagnosis': bool(diagnosis),
    }
