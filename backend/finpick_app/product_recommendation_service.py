import json

from django.conf import settings

from .ai_services import (
    build_today_message,
    diagnosis_context,
    format_guides_for_prompt,
    get_diagnosis_area_scores,
    search_financial_guides,
)
from .models import DepositProduct, DiagnosisResult


class OpenAIUnavailableError(Exception):
    pass


OpenAIError = OpenAIUnavailableError


class _UnavailableOpenAICompletions:
    def create(self, *args, **kwargs):
        raise OpenAIUnavailableError("openai package is not installed.")


class _UnavailableOpenAIChat:
    completions = _UnavailableOpenAICompletions()


class _UnavailableOpenAIClient:
    chat = _UnavailableOpenAIChat()


def get_openai_client():
    global OpenAIError

    try:
        from openai import OpenAI as ImportedOpenAI, OpenAIError as ImportedOpenAIError
    except ImportError:
        return _UnavailableOpenAIClient()

    OpenAIError = ImportedOpenAIError
    return ImportedOpenAI(api_key=settings.GMS_API_KEY, base_url=settings.GMS_OPENAI_BASE_URL)


def number(value, default=0):
    try:
        return float(value or default)
    except (TypeError, ValueError):
        return default


def best_option(product):
    return product.options.order_by('-max_interest_rate', '-interest_rate', 'saving_term').first()


def monthly_saving_capacity(user):
    profile = getattr(user, 'profile', None)
    income = getattr(profile, 'monthly_income', None) or 0
    expense = getattr(profile, 'monthly_expense', None) or 0
    try:
        return max(0, int(income) - int(expense))
    except (TypeError, ValueError):
        return 0


def serialize_scored_product(product, user, score, reasons):
    option = best_option(product)
    return {
        'id': product.id,
        'product_type': product.product_type,
        'product_type_display': product.get_product_type_display(),
        'financial_company_name': product.financial_company_name,
        'product_name': product.product_name,
        'join_way': product.join_way,
        'max_limit': product.max_limit,
        'best_term': option.saving_term if option else None,
        'interest_rate': str(option.interest_rate) if option and option.interest_rate is not None else None,
        'max_interest_rate': str(option.max_interest_rate) if option and option.max_interest_rate is not None else None,
        'recommendation_score': round(score, 2),
        'score_reasons': reasons,
    }


def score_deposit_product(product, diagnosis, user):
    scores = get_diagnosis_area_scores(diagnosis) if diagnosis else {}
    option = best_option(product)
    rate = number(getattr(option, 'max_interest_rate', None) or getattr(option, 'interest_rate', None))
    term = int(getattr(option, 'saving_term', None) or 0)
    capacity = monthly_saving_capacity(user)
    score = rate * 8
    reasons = []

    if product.product_type in ['deposit', 'saving']:
        score += 20
        reasons.append('예금/적금처럼 구조가 단순한 안정형 상품입니다.')

    investment_score = scores.get('투자', 0)
    stability_score = scores.get('안정성', 0)
    if investment_score < 70:
        score += 18
        reasons.append('투자 경험이 충분하지 않은 사용자에게 안정적인 시작점이 됩니다.')
    if stability_score < 70:
        score += 18
        reasons.append('안정성 보완이 필요한 사용자에게 원금 손실 가능성이 낮은 편입니다.')

    if capacity and (not product.max_limit or capacity <= product.max_limit):
        score += 10
        reasons.append('월 저축 가능 금액 안에서 검토하기 쉽습니다.')

    if 6 <= term <= 12:
        score += 12
        reasons.append('6~12개월 단기 목표 자금 관리에 적합한 기간입니다.')
    elif term and term <= 24:
        score += 6

    if rate >= 3:
        score += 8
        reasons.append('후보군 안에서 금리 경쟁력이 있습니다.')

    readiness = int(getattr(diagnosis, 'readiness_score', None) or 0)
    if readiness < 60 and product.product_type in ['deposit', 'saving']:
        score += 10
        reasons.append('금융 레벨이 낮을수록 복잡한 상품보다 이해하기 쉽습니다.')

    return score, reasons[:4]


def select_recommended_deposit_products(user, limit=5):
    diagnosis = DiagnosisResult.objects.filter(user=user).order_by('-created_at').first()
    products = DepositProduct.objects.prefetch_related('options').all()
    ranked = []
    for product in products:
        score, reasons = score_deposit_product(product, diagnosis, user)
        ranked.append((score, product, reasons))
    ranked.sort(key=lambda item: item[0], reverse=True)
    selected = [
        serialize_scored_product(product, user, score, reasons)
        for score, product, reasons in ranked[:limit]
    ]
    return selected, diagnosis


def build_ai_recommendation_reasons(user, products, diagnosis):
    if not products:
        return {}

    guides = search_financial_guides(['저축', '안정성', '사회초년생'], limit=4)
    prompt = f"""
역할: 사회초년생을 위한 금융 코치

입력: 사용자의 금융진단 결과
{json.dumps(diagnosis_context(diagnosis), ensure_ascii=False) if diagnosis else '진단 결과 없음'}

추천 후보 상품:
{json.dumps(products, ensure_ascii=False)}

[참고 금융 가이드]
{format_guides_for_prompt(guides)}

제약조건:
- 추천 상품 자체는 이미 백엔드 점수화로 선정되었으므로 다른 상품을 고르지 않기
- 각 상품이 사용자에게 적합한 이유만 작성
- 과장된 투자 권유 금지
- 원금 손실 가능 상품에 대해 단정적으로 추천 금지
- 없는 정보를 지어내지 않기

출력 형식:
{{"recommendations":[{{"id":1,"reason":"..."}}]}}
"""
    fallback = {}
    if not settings.GMS_API_KEY or not settings.GMS_OPENAI_BASE_URL:
        return fallback

    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model=settings.GMS_OPENAI_MODEL,
            messages=[
                {'role': 'system', 'content': '당신은 사회초년생을 위한 금융 코치입니다.'},
                {'role': 'user', 'content': prompt},
            ],
            temperature=0.35,
            response_format={'type': 'json_object'},
        )
        payload = json.loads(response.choices[0].message.content or '{}')
    except (OpenAIError, json.JSONDecodeError, TypeError, ValueError):
        return fallback

    reasons = {}
    for item in payload.get('recommendations', []):
        try:
            product_id = int(item.get('id'))
        except (TypeError, ValueError):
            continue
        reason = ' '.join(str(item.get('reason') or '').split())
        if reason:
            reasons[product_id] = reason
    return reasons


def get_scored_product_recommendations(user):
    products, diagnosis = select_recommended_deposit_products(user)
    if not products:
        return {
            'products': [],
            'financial_type': diagnosis.financial_type if diagnosis else '',
            'message': '추천 가능한 예적금 상품이 없습니다.',
            'has_diagnosis': bool(diagnosis),
        }

    ai_reasons = build_ai_recommendation_reasons(user, products, diagnosis)
    for product in products:
        reason = ai_reasons.get(product['id'])
        if reason:
            product['recommendation_reason'] = reason

    today = build_today_message(user)
    return {
        'products': products,
        'deposits': products,
        'stocks': [],
        'financial_type': diagnosis.financial_type if diagnosis else '금융 새싹',
        'message': f'{diagnosis.financial_type if diagnosis else "금융 새싹"} 유형 기준 오늘의 추천 상품이에요.',
        'today_message': today['message'],
        'has_diagnosis': bool(diagnosis),
    }
