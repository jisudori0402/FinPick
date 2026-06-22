from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import (
    DiagnosisResult,
    ProductRecommendation,
    RoadmapMission,
    RoadmapStep,
    RoadmapTemplate,
    UserMission,
    UserProfile,
)


TYPE_CONTENT = {
    '🐢 안정형 저축러': {
        'intro': '원금 손실을 최소화하며 꾸준한 저축으로 자산을 쌓는 유형입니다.',
        'comment': '지금처럼 안정적인 저축을 유지하면서 CMA나 ETF 같은 상품도 천천히 경험해보세요.',
    },
    '🐿 계획형 목돈러': {
        'intro': '명확한 목표를 세우고 꾸준히 목돈을 모으는 유형입니다.',
        'comment': '목돈 마련이 강점인 만큼 청년도약계좌나 ISA를 활용해보세요.',
    },
    '🦊 똑똑한 소비러': {
        'intro': '소비는 많지만 혜택 활용 능력이 뛰어난 유형입니다.',
        'comment': '카드 혜택과 소비 관리만 잘해도 생각보다 많은 돈을 아낄 수 있어요.',
    },
    '🐯 성장형 투자러': {
        'intro': '저축보다 자산 증식을 목표로 하는 성장형 투자자입니다.',
        'comment': '투자는 꾸준함이 중요합니다. 장기 관점으로 접근해보세요.',
    },
    '🐻 재정 점검러': {
        'intro': '투자보다 현금 흐름과 재정 안정화가 먼저 필요한 유형입니다.',
        'comment': '지금은 투자보다 비상금과 현금 흐름 관리가 먼저입니다.',
    },
    '🦁 공격형 자산러': {
        'intro': '높은 수익을 위해 적극적으로 투자하는 자산 성장형 유형입니다.',
        'comment': '높은 수익도 중요하지만 리스크 관리가 장기 수익률을 결정합니다.',
    },
}

ROADMAP_TEMPLATES = {
    '🐢 안정형 저축러': [
        ('Lv.1 금융 기초', '현재 재무 상태 파악 및 금융 목표 설정', ['월 고정지출 확인하기', '비상금 목표 설정하기', '소비 패턴 분석하기']),
        ('Lv.2 금융 습관', '저축 및 소비 습관 형성', ['월급의 20% 자동저축 설정하기', '적금 가입하기', '비상금 300만원 달성하기']),
        ('Lv.3 자산 성장', '금융상품 활용 및 자산 증식', ['주택청약 가입 여부 확인하기', 'CMA 계좌 활용하기', '예금 상품 비교하기']),
    ],
    '🐿 계획형 목돈러': [
        ('Lv.1 금융 기초', '현재 재무 상태 파악 및 금융 목표 설정', ['목표 금액 설정하기', '월 저축 가능 금액 계산하기', '소비 패턴 분석하기']),
        ('Lv.2 금융 습관', '저축 및 소비 습관 형성', ['월급의 20% 자동저축 설정하기', '목적별 통장 분리하기', '적금 상품 비교하기']),
        ('Lv.3 자산 성장', '금융상품 활용 및 자산 증식', ['청년도약계좌 알아보기', '주택청약 가입 여부 확인하기', 'ISA 계좌 알아보기']),
    ],
    '🦊 똑똑한 소비러': [
        ('Lv.1 금융 기초', '현재 재무 상태 파악 및 금융 목표 설정', ['월 소비 내역 확인하기', '고정지출 확인하기', '소비 카테고리 분석하기']),
        ('Lv.2 금융 습관', '저축 및 소비 습관 형성', ['소비 예산 설정하기', '카드 혜택 비교하기', '불필요한 구독 서비스 정리하기']),
        ('Lv.3 자산 성장', '금융상품 활용 및 자산 증식', ['절약 금액 저축하기', '적금 가입하기', '비상금 만들기']),
    ],
    '🐯 성장형 투자러': [
        ('Lv.1 금융 기초', '현재 재무 상태 파악 및 금융 목표 설정', ['비상금 확보하기', '투자 목표 설정하기', '투자 공부 시작하기']),
        ('Lv.2 금융 습관', '저축 및 소비 습관 형성', ['증권계좌 개설하기', 'ISA 계좌 알아보기', 'ETF 상품 비교하기']),
        ('Lv.3 자산 성장', '금융상품 활용 및 자산 증식', ['ETF 분산투자 시작하기', '투자 포트폴리오 구성하기', '투자 성과 점검하기']),
    ],
    '🐻 재정 점검러': [
        ('Lv.1 금융 기초', '현재 재무 상태 파악 및 금융 목표 설정', ['월 지출 분석하기', '고정비 확인하기', '대출 현황 확인하기']),
        ('Lv.2 금융 습관', '저축 및 소비 습관 형성', ['소비 예산 설정하기', '대출 상환 계획 세우기', '비상금 목표 설정하기']),
        ('Lv.3 자산 성장', '금융상품 활용 및 자산 증식', ['비상금 100만원 만들기', '적금 가입하기', '금융 목표 설정하기']),
    ],
    '🦁 공격형 자산러': [
        ('Lv.1 금융 기초', '현재 재무 상태 파악 및 금융 목표 설정', ['투자 목표 설정하기', '투자 가능 금액 계산하기', '투자 포트폴리오 설계하기']),
        ('Lv.2 금융 습관', '저축 및 소비 습관 형성', ['국내 ETF 투자하기', '해외 ETF 투자하기', 'ISA 활용하기']),
        ('Lv.3 자산 성장', '금융상품 활용 및 자산 증식', ['자산 비중 점검하기', '투자 성과 분석하기', '리밸런싱 진행하기']),
    ],
}

ROADMAP_COMMENTS = {
    '🐢 안정형 저축러': '이번 달에는 자동저축 설정과 비상금 목표 달성을 우선 추천드려요.',
    '🐿 계획형 목돈러': '이번 달에는 비상금 마련과 자동저축 설정을 우선 추천드려요.',
    '🦊 똑똑한 소비러': '이번 달에는 소비 예산 설정과 불필요한 구독 정리를 우선 추천드려요.',
    '🐯 성장형 투자러': '이번 달에는 비상금 확보와 ETF 기초 학습을 우선 추천드려요.',
    '🐻 재정 점검러': '이번 달에는 지출 분석과 대출 상환 계획을 우선 추천드려요.',
    '🦁 공격형 자산러': '이번 달에는 포트폴리오 점검과 리밸런싱 기준 설정을 우선 추천드려요.',
}


def index(request):
    roadmap = list(RoadmapStep.objects.values('step_number', 'title', 'description'))
    products = list(ProductRecommendation.objects.values('name', 'product_type', 'reason', 'category'))
    latest_diagnosis = None
    if request.user.is_authenticated:
        latest_diagnosis = (
            DiagnosisResult.objects.filter(user=request.user)
            .order_by('-created_at')
            .first()
        )

    return render(request, 'index.html', {
        'user': request.user,
        'initial_roadmap': roadmap,
        'initial_products': products,
        'latest_diagnosis': latest_diagnosis,
        'latest_result': diagnosis_to_payload(latest_diagnosis) if latest_diagnosis else None,
    })


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        birth_date_value = request.POST.get('birth_date', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not name or not email or not birth_date_value or not password1 or not password2:
            messages.error(request, '필수 정보를 모두 입력해 주세요.')
            return render(request, 'signup.html')
        if password1 != password2:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'signup.html')
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            messages.error(request, '이미 사용 중인 이메일입니다.')
            return render(request, 'signup.html')

        try:
            birth_date = datetime.strptime(birth_date_value, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, '생년월일 형식이 올바르지 않습니다.')
            return render(request, 'signup.html')

        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=name,
        )
        UserProfile.objects.create(user=user, birth_date=birth_date, age=age)
        login(request, user)
        return redirect('index')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '로그인되었습니다.')
            return redirect('index')
        messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, '로그아웃되었습니다.')
    return redirect('index')


@login_required
def dashboard_view(request):
    profile = getattr(request.user, 'profile', None)
    return render(request, 'dashboard.html', {'profile': profile})


def get_financial_scores(income_level, spending_style, investment_style, asset_level, loan_type):
    income_scores = {
        '200만원 미만': 8,
        '200~300만원': 12,
        '300~400만원': 16,
        '400~500만원': 18,
        '500만원 이상': 20,
    }
    spending_scores = {
        '월급 들어오면 바로 쓴다': 5,
        '필요한 만큼만 쓴다': 15,
        '계획적으로 소비한다': 18,
        '저축을 우선한다': 20,
    }
    investment_scores = {
        '원금 손실은 절대 싫다': 8,
        '조금은 감수 가능': 12,
        '수익을 위해 위험 감수 가능': 16,
        '공격적으로 투자하고 싶다': 20,
    }
    asset_scores = {
        '500만원 미만': 5,
        '500~1,000만원': 10,
        '1,000~3,000만원': 16,
        '3,000만원 이상': 20,
    }
    debt_scores = {
        '없음': 20,
        '학자금 대출': 12,
        '전세 대출': 14,
        '신용 대출': 8,
        '기타': 10,
    }

    return {
        'income': income_scores.get(income_level, 0),
        'spending': spending_scores.get(spending_style, 0),
        'investment': investment_scores.get(investment_style, 0),
        'asset': asset_scores.get(asset_level, 0),
        'debt': debt_scores.get(loan_type, 0),
    }


def decide_financial_type(financial_goal, spending_style, investment_style, asset_level, loan_type, readiness_score):
    asset_under_10m = asset_level in ['500만원 미만', '500~1,000만원']
    asset_over_10m = asset_level in ['1,000~3,000만원', '3,000만원 이상']
    has_debt = loan_type != '없음'
    risk_possible = investment_style in ['수익을 위해 위험 감수 가능', '공격적으로 투자하고 싶다']

    if asset_under_10m and has_debt and readiness_score < 60:
        return '🐻 재정 점검러'
    if investment_style == '공격적으로 투자하고 싶다' and asset_over_10m:
        return '🦁 공격형 자산러'
    if financial_goal == '투자 시작하기' and risk_possible:
        return '🐯 성장형 투자러'
    if spending_style == '저축을 우선한다' and investment_style == '원금 손실은 절대 싫다':
        return '🐢 안정형 저축러'
    if financial_goal in ['결혼 자금 준비', '내 집 마련', '여행 자금 모으기']:
        return '🐿 계획형 목돈러'
    if spending_style in ['필요한 만큼만 쓴다', '계획적으로 소비한다']:
        return '🦊 똑똑한 소비러'
    return '🐢 안정형 저축러'


def build_strengths(scores):
    strengths = []
    if scores['spending'] >= 15:
        strengths.append('계획적인 소비 습관이 있어요')
    if scores['asset'] >= 15:
        strengths.append('자산 관리 기반이 잘 갖춰져 있어요')
    if scores['debt'] >= 15:
        strengths.append('안정적인 재무 상태를 유지하고 있어요')
    if scores['income'] >= 16:
        strengths.append('안정적인 소득 기반을 보유하고 있어요')
    return strengths or ['현재 재정 상태를 점검하려는 의지가 있어요']


def build_improvements(scores):
    improvements = []
    if scores['investment'] <= 10:
        improvements.append('투자 경험이 부족해요')
    if scores['spending'] <= 10:
        improvements.append('소비 습관 개선이 필요해요')
    if scores['debt'] <= 10:
        improvements.append('부채 관리가 필요해요')
    if scores['asset'] <= 10:
        improvements.append('자산 형성 전략이 필요해요')
    return improvements or ['현재의 좋은 흐름을 꾸준히 유지해보세요']


def score_to_stars(score):
    filled = max(1, min(5, round(score / 4)))
    return '★' * filled + '☆' * (5 - filled)


def diagnosis_to_payload(result):
    return {
        'id': result.id,
        'financial_type': result.financial_type or result.level,
        'intro': result.summary,
        'readiness_score': result.readiness_score or 0,
        'profile_scores': result.profile_scores or {},
        'strengths': result.strengths.splitlines() if result.strengths else [],
        'improvements': result.improvements.splitlines() if result.improvements else [],
        'finpick_comment': result.finpick_comment,
    }


def get_latest_financial_type(user):
    latest = DiagnosisResult.objects.filter(user=user).order_by('-created_at').first()
    if latest and latest.financial_type:
        return latest.financial_type
    return '🐿 계획형 목돈러'


def ensure_roadmap_for_type(type_code):
    levels = ROADMAP_TEMPLATES.get(type_code, ROADMAP_TEMPLATES['🐿 계획형 목돈러'])
    for level_index, (title, description, missions) in enumerate(levels, start=1):
        template, _ = RoadmapTemplate.objects.update_or_create(
            type_code=type_code,
            level=level_index,
            defaults={
                'title': title,
                'description': description,
                'order': level_index,
            },
        )
        for mission_index, mission_title in enumerate(missions, start=1):
            RoadmapMission.objects.update_or_create(
                roadmap_template=template,
                mission_title=mission_title,
                defaults={
                    'mission_description': '',
                    'category': title,
                    'order': mission_index,
                },
            )


def get_user_roadmap(user):
    type_code = get_latest_financial_type(user)
    ensure_roadmap_for_type(type_code)
    templates = RoadmapTemplate.objects.filter(type_code=type_code).prefetch_related('missions').order_by('order')
    mission_ids = [mission.id for template in templates for mission in template.missions.all()]
    for mission_id in mission_ids:
        UserMission.objects.get_or_create(user=user, mission_id=mission_id)

    user_missions = {
        user_mission.mission_id: user_mission
        for user_mission in UserMission.objects.filter(user=user, mission_id__in=mission_ids)
    }
    completed_count = sum(1 for user_mission in user_missions.values() if user_mission.is_completed)
    total_count = len(mission_ids)
    progress = round((completed_count / total_count) * 100) if total_count else 0

    level_completion = {}
    for template in templates:
        template_missions = list(template.missions.all())
        level_completion[template.level] = all(
            user_missions[mission.id].is_completed for mission in template_missions
        )

    unlocked_level = 1
    if level_completion.get(1):
        unlocked_level = 2
    if level_completion.get(1) and level_completion.get(2):
        unlocked_level = 3

    levels = []
    for template in templates:
        if template.level > unlocked_level:
            continue

        is_locked = template.level < unlocked_level
        missions = []
        for mission in template.missions.all():
            user_mission = user_missions[mission.id]
            missions.append({
                'id': mission.id,
                'title': mission.mission_title,
                'description': mission.mission_description,
                'category': mission.category,
                'order': mission.order,
                'is_completed': user_mission.is_completed,
                'is_locked': is_locked,
            })
        levels.append({
            'id': template.id,
            'level': template.level,
            'title': template.title,
            'description': template.description,
            'is_locked': is_locked,
            'missions': missions,
        })

    name = user.first_name or user.username
    type_name = type_code.split(' ', 1)[1] if ' ' in type_code else type_code
    return {
        'type_code': type_code,
        'progress': progress,
        'completed_count': completed_count,
        'total_count': total_count,
        'comment': f'{name}님은 {type_name}입니다. {ROADMAP_COMMENTS.get(type_code, ROADMAP_COMMENTS["🐿 계획형 목돈러"])}',
        'levels': levels,
    }


@csrf_exempt
@login_required
def api_diagnosis(request):
    if request.method == 'POST':
        data = request.POST
        income_level = data.get('income_level', '').strip()
        spending_style = data.get('spending_style', '').strip()
        financial_goal = data.get('financial_goal', '').strip()
        investment_style = data.get('investment_style', '').strip()
        asset_level = data.get('asset_level', '').strip()
        loan_type = data.get('loan_type', '').strip()

        if not all([income_level, spending_style, financial_goal, investment_style, asset_level, loan_type]):
            return JsonResponse({'message': '모든 진단 항목을 선택해 주세요.'}, status=400)

        scores = get_financial_scores(income_level, spending_style, investment_style, asset_level, loan_type)
        readiness_score = sum(scores.values())
        financial_type = decide_financial_type(
            financial_goal,
            spending_style,
            investment_style,
            asset_level,
            loan_type,
            readiness_score,
        )
        strengths = build_strengths(scores)
        improvements = build_improvements(scores)
        type_content = TYPE_CONTENT[financial_type]
        profile_scores = {
            '저축 습관': score_to_stars(max(scores['spending'], scores['asset'])),
            '소비 관리': score_to_stars(scores['spending']),
            '투자 성향': score_to_stars(scores['investment']),
            '자산 관리': score_to_stars(scores['asset']),
        }
        comment = type_content['comment']

        result = DiagnosisResult.objects.create(
            user=request.user,
            income=income_level,
            expense=spending_style,
            saving=financial_goal,
            invest=investment_style,
            income_level=income_level,
            spending_style=spending_style,
            financial_goal=financial_goal,
            investment_style=investment_style,
            asset_level=asset_level,
            loan_type=loan_type,
            financial_type=financial_type,
            readiness_score=readiness_score,
            strengths='\n'.join(strengths),
            improvements='\n'.join(improvements),
            finpick_comment=comment,
            profile_scores=profile_scores,
            level=financial_type,
            summary=type_content['intro'],
        )

        return JsonResponse(diagnosis_to_payload(result))
    return JsonResponse({'message': 'POST 요청만 지원합니다.'}, status=405)


@login_required
def api_roadmap(request):
    return JsonResponse({'roadmap': get_user_roadmap(request.user)})


@csrf_exempt
@login_required
def api_user_mission(request, mission_id):
    if request.method != 'POST':
        return JsonResponse({'message': 'POST 요청만 지원합니다.'}, status=405)

    type_code = get_latest_financial_type(request.user)
    ensure_roadmap_for_type(type_code)
    mission = RoadmapMission.objects.filter(id=mission_id, roadmap_template__type_code=type_code).first()
    if mission is None:
        return JsonResponse({'message': '미션을 찾을 수 없습니다.'}, status=404)

    user_mission, _ = UserMission.objects.get_or_create(user=request.user, mission=mission)
    if user_mission.is_completed:
        roadmap = get_user_roadmap(request.user)
        current_level = max((level['level'] for level in roadmap['levels']), default=1)
        if mission.roadmap_template.level < current_level:
            return JsonResponse({'message': '이전 레벨 미션은 완료 해제할 수 없습니다.', 'roadmap': roadmap}, status=400)

    user_mission.is_completed = not user_mission.is_completed
    user_mission.completed_at = timezone.now() if user_mission.is_completed else None
    user_mission.save(update_fields=['is_completed', 'completed_at'])
    return JsonResponse({'roadmap': get_user_roadmap(request.user)})


def api_products(request):
    products = list(ProductRecommendation.objects.values('name', 'product_type', 'reason', 'category'))
    return JsonResponse({'products': products})
