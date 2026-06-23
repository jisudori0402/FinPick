from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import json
from django.contrib.auth import get_user_model

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib.auth import authenticate, login

from .models import (
    DepositProduct,
    DiagnosisResult,
    ProductRecommendation,
    RoadmapMission,
    RoadmapStep,
    RoadmapTemplate,
    UserMission,
    UserDepositSubscription,
    UserProfile,
    CommunityPost,
    CommunityComment,
    UserFavoriteDepositProduct,
)


XLSX_NS = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
SPOT_PRICE_FILES = {
    'gold': {
        'name': '금',
        'path': Path.home() / 'Downloads' / 'Gold_prices.xlsx',
    },
    'silver': {
        'name': '은',
        'path': Path.home() / 'Downloads' / 'Silver_prices.xlsx',
    },
}


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
        ('Lv.1 금융 진단', '현재 재무상태를 파악합니다.', ['월 고정지출 확인하기', '최근 3개월 소비 분석하기', '금융 목표 설정하기']),
        ('Lv.2 금융 기초', '저축과 소비의 기본 습관을 만듭니다.', ['비상금 목표 설정하기', '월급의 20% 자동저축 설정하기', '소비 예산 작성하기']),
        ('Lv.3 목돈 준비', '안정적인 목돈 형성을 시작합니다.', ['적금 상품 가입하기', '비상금 300만원 달성하기', '생활비 통장 분리하기']),
        ('Lv.4 자산 성장', '금융상품을 활용해 자산을 키웁니다.', ['CMA 계좌 개설하기', '예금 상품 비교하기', '주택청약 가입 여부 확인하기']),
        ('Lv.5 금융 완성', '장기 자산 관리 체계를 만듭니다.', ['연간 자산 점검하기', 'ISA 계좌 알아보기', '자산 포트폴리오 구성하기']),
    ],
    '🐿 계획형 목돈러': [
        ('Lv.1 금융 진단', '목표 자금 마련을 위한 현재 상태를 점검합니다.', ['목표 금액 설정하기', '목표 달성 기간 설정하기', '월 저축 가능 금액 계산하기']),
        ('Lv.2 금융 기초', '목표 달성을 방해하는 소비 흐름을 정리합니다.', ['소비 패턴 분석하기', '고정지출 줄이기', '월 예산 계획 세우기']),
        ('Lv.3 목돈 준비', '목적별 저축 구조를 만듭니다.', ['월급의 20% 자동저축 설정하기', '목적별 통장 만들기', '적금 상품 가입하기']),
        ('Lv.4 자산 성장', '목돈 마련에 맞는 금융상품을 활용합니다.', ['청년도약계좌 알아보기', 'ISA 계좌 알아보기', '주택청약 가입 여부 확인하기']),
        ('Lv.5 금융 완성', '목표 달성 이후의 장기 계획을 세웁니다.', ['목표 달성률 점검하기', '투자 공부 시작하기', '장기 재무계획 세우기']),
    ],
    '🦊 똑똑한 소비러': [
        ('Lv.1 금융 진단', '소비 흐름을 정확히 파악합니다.', ['월 소비 내역 확인하기', '소비 카테고리 분석하기', '고정지출 확인하기']),
        ('Lv.2 금융 기초', '불필요한 지출을 줄이는 습관을 만듭니다.', ['소비 예산 설정하기', '불필요한 지출 찾기', '구독 서비스 정리하기']),
        ('Lv.3 목돈 준비', '절약한 금액을 저축으로 연결합니다.', ['카드 혜택 비교하기', '절약 목표 설정하기', '절약 금액 자동저축하기']),
        ('Lv.4 자산 성장', '기초 자산 형성을 시작합니다.', ['비상금 100만원 만들기', '적금 가입하기', '금융 목표 설정하기']),
        ('Lv.5 금융 완성', '자산과 소비를 함께 관리합니다.', ['자산 현황 점검하기', 'ISA 계좌 알아보기', '투자 공부 시작하기']),
    ],
    '🐯 성장형 투자러': [
        ('Lv.1 금융 진단', '투자를 시작하기 전 기본 상태를 점검합니다.', ['투자 가능 금액 계산하기', '금융 목표 설정하기', '투자 성향 확인하기']),
        ('Lv.2 금융 기초', '투자 전 안전장치를 마련합니다.', ['비상금 확보하기', '소비 예산 설정하기', '투자 공부 시작하기']),
        ('Lv.3 목돈 준비', '투자 계좌와 상품을 이해합니다.', ['증권계좌 개설하기', 'ISA 계좌 알아보기', 'ETF 상품 비교하기']),
        ('Lv.4 자산 성장', '소액으로 분산 투자를 시작합니다.', ['ETF 투자 시작하기', '분산 투자하기', '투자 기록 작성하기']),
        ('Lv.5 금융 완성', '투자 성과를 점검하고 조정합니다.', ['포트폴리오 점검하기', '투자 성과 분석하기', '리밸런싱 진행하기']),
    ],
    '🐻 재정 점검러': [
        ('Lv.1 금융 진단', '지출과 대출 현황을 확인합니다.', ['월 지출 분석하기', '고정비 확인하기', '대출 현황 확인하기']),
        ('Lv.2 금융 기초', '재무 안정화를 위한 지출 계획을 세웁니다.', ['소비 예산 설정하기', '지출 줄이기 계획 세우기', '금융 목표 설정하기']),
        ('Lv.3 목돈 준비', '대출 상환과 비상금 마련을 병행합니다.', ['대출 상환 계획 세우기', '비상금 목표 설정하기', '월 저축 습관 만들기']),
        ('Lv.4 자산 성장', '기초 자산과 신용 관리를 시작합니다.', ['비상금 100만원 만들기', '적금 가입하기', '신용점수 확인하기']),
        ('Lv.5 금융 완성', '장기 재무 계획을 정리합니다.', ['대출 상환률 점검하기', '자산 현황 정리하기', '장기 재무계획 세우기']),
    ],
    '🦁 공격형 자산러': [
        ('Lv.1 금융 진단', '공격적 자산 증식을 위한 기본 상태를 점검합니다.', ['투자 목표 설정하기', '자산 현황 점검하기', '투자 가능 금액 계산하기']),
        ('Lv.2 금융 기초', '리스크 관리를 위한 원칙을 세웁니다.', ['비상금 확보하기', '투자 원칙 정하기', '포트폴리오 설계하기']),
        ('Lv.3 목돈 준비', 'ETF와 ISA를 활용한 투자 기반을 만듭니다.', ['국내 ETF 투자하기', '해외 ETF 투자하기', 'ISA 계좌 활용하기']),
        ('Lv.4 자산 성장', '투자 성과와 리스크를 관리합니다.', ['자산 비중 점검하기', '투자 성과 분석하기', '리스크 관리하기']),
        ('Lv.5 금융 완성', '장기 투자 전략을 완성합니다.', ['포트폴리오 리밸런싱', '장기 투자 전략 수립', '연간 수익률 점검하기']),
    ],
}

ROADMAP_COMMENTS = {
    '🐢 안정형 저축러': '이번 달에는 비상금 마련과 자동저축 설정을 우선 추천드려요.',
    '🐿 계획형 목돈러': '이번 달에는 비상금 마련과 자동저축 설정을 우선 추천드려요.',
    '🦊 똑똑한 소비러': '이번 달에는 소비 예산 설정과 구독 서비스 정리를 우선 추천드려요.',
    '🐯 성장형 투자러': '이번 달에는 비상금 확보와 투자 공부 시작을 우선 추천드려요.',
    '🐻 재정 점검러': '이번 달에는 지출 분석과 대출 상환 계획을 우선 추천드려요.',
    '🦁 공격형 자산러': '이번 달에는 투자 원칙 정하기와 포트폴리오 설계를 우선 추천드려요.',
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
        'kakao_map_app_key': settings.KAKAO_MAP_APP_KEY,
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
    if latest and latest.financial_type in ROADMAP_TEMPLATES:
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
        RoadmapMission.objects.filter(roadmap_template=template).exclude(
            mission_title__in=missions
        ).delete()
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
    for template in templates:
        if template.level == unlocked_level and level_completion.get(template.level):
            unlocked_level += 1
    max_level = max((template.level for template in templates), default=1)
    unlocked_level = min(unlocked_level, max_level)

    levels = []
    for template in templates:
        is_future_level = template.level > unlocked_level
        is_past_level = template.level < unlocked_level
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
                'is_locked': is_future_level or is_past_level,
            })
        levels.append({
            'id': template.id,
            'level': template.level,
            'title': template.title,
            'description': template.description,
            'is_locked': is_future_level,
            'is_past': is_past_level,
            'missions': missions,
        })

    name = user.first_name or user.username
    type_name = type_code.split(' ', 1)[1] if ' ' in type_code else type_code
    comment = ROADMAP_COMMENTS.get(type_code, ROADMAP_COMMENTS['🐿 계획형 목돈러'])
    return {
        'type_code': type_code,
        'progress': progress,
        'completed_count': completed_count,
        'total_count': total_count,
        'comment': f'{name}님은 {type_name}입니다. {comment}',
        'levels': levels,
    }


@csrf_exempt
@login_required
def api_diagnosis(request):
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type', '')

        if content_type.startswith('application/json'):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'message': '?섎せ???붿껌 ?뺤떇?낅땲??'}, status=400)
        else:
            data = request.POST

        income_level = (data.get('income_level') or '').strip()
        spending_style = (data.get('spending_style') or '').strip()
        financial_goal = (data.get('financial_goal') or '').strip()
        investment_style = (data.get('investment_style') or '').strip()
        asset_level = (data.get('asset_level') or '').strip()
        loan_type = (data.get('loan_type') or '').strip()

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

        return JsonResponse({
            'message': '吏꾨떒???꾨즺?섏뿀?듬땲??',
            'result': diagnosis_to_payload(result),
        }, status=201)
    return JsonResponse({'message': 'POST 요청만 지원합니다.'}, status=405)


@login_required
def api_latest_diagnosis(request):
    latest_diagnosis = (
        DiagnosisResult.objects.filter(user=request.user)
        .order_by('-created_at')
        .first()
    )

    return JsonResponse({
        'result': diagnosis_to_payload(latest_diagnosis) if latest_diagnosis else None,
    })


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

    roadmap = get_user_roadmap(request.user)
    level = next(
        (
            level
            for level in roadmap['levels']
            if level['level'] == mission.roadmap_template.level
        ),
        None,
    )
    mission_state = next(
        (
            mission
            for mission in level['missions']
            if mission['id'] == mission_id
        ),
        None,
    ) if level else None
    if mission_state and mission_state['is_locked']:
        message = '이미 완료한 이전 레벨의 미션은 변경할 수 없습니다.'
        if level and level['is_locked']:
            message = '이전 레벨의 미션을 모두 완료하면 다음 레벨이 열립니다.'
        return JsonResponse({'message': message, 'roadmap': roadmap}, status=400)

    user_mission, _ = UserMission.objects.get_or_create(user=request.user, mission=mission)
    user_mission.is_completed = not user_mission.is_completed
    user_mission.completed_at = timezone.now() if user_mission.is_completed else None
    user_mission.save(update_fields=['is_completed', 'completed_at'])
    return JsonResponse({'roadmap': get_user_roadmap(request.user)})


def api_products(request):
    products = list(ProductRecommendation.objects.values('name', 'product_type', 'reason', 'category'))
    return JsonResponse({'products': products})


def serialize_comment(comment, user=None):
    return {
        'id': comment.id,
        'content': comment.content,
        'author': comment.author.get_full_name() or comment.author.username,
        'created_at': timezone.localtime(comment.created_at).strftime('%Y-%m-%d %H:%M'),
        'can_edit': bool(user and user.is_authenticated and comment.author_id == user.id),
    }


def serialize_post(post, user=None, include_comments=False):
    payload = {
        'id': post.id,
        'board': post.board,
        'board_label': post.get_board_display(),
        'title': post.title,
        'content': post.content,
        'author': post.author.get_full_name() or post.author.username,
        'created_at': timezone.localtime(post.created_at).strftime('%Y-%m-%d %H:%M'),
        'comment_count': getattr(post, 'comment_count', post.comments.count()),
        'can_edit': bool(user and user.is_authenticated and post.author_id == user.id),
    }
    if include_comments:
        payload['comments'] = [
            serialize_comment(comment, user)
            for comment in post.comments.select_related('author')
        ]
    return payload


@csrf_exempt
@login_required
def api_community_posts(request):
    if request.method == 'GET':
        board = request.GET.get('board', '').strip()
        posts = CommunityPost.objects.select_related('author').prefetch_related('comments')
        if board:
            posts = posts.filter(board=board)
        return JsonResponse({
            'posts': [serialize_post(post, request.user) for post in posts],
            'boards': [{'value': value, 'label': label} for value, label in CommunityPost.BOARD_CHOICES],
        })

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        board = request.POST.get('board', 'free').strip()
        if board not in dict(CommunityPost.BOARD_CHOICES):
            board = 'free'
        if not title or not content:
            return JsonResponse({'message': '제목과 내용을 입력해 주세요.'}, status=400)
        post = CommunityPost.objects.create(
            author=request.user,
            board=board,
            title=title,
            content=content,
        )
        return JsonResponse({'post': serialize_post(post, request.user, include_comments=True)}, status=201)

    return JsonResponse({'message': '지원하지 않는 요청입니다.'}, status=405)


@csrf_exempt
@login_required
def api_community_post_detail(request, post_id):
    post = CommunityPost.objects.select_related('author').filter(id=post_id).first()
    if post is None:
        return JsonResponse({'message': '게시글을 찾을 수 없습니다.'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'post': serialize_post(post, request.user, include_comments=True)})

    if request.method == 'POST':
        if post.author_id != request.user.id:
            return JsonResponse({'message': '본인이 작성한 게시글만 수정할 수 있습니다.'}, status=403)
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        board = request.POST.get('board', post.board).strip()
        if board not in dict(CommunityPost.BOARD_CHOICES):
            board = post.board
        if not title or not content:
            return JsonResponse({'message': '제목과 내용을 입력해 주세요.'}, status=400)
        post.title = title
        post.content = content
        post.board = board
        post.save(update_fields=['title', 'content', 'board', 'updated_at'])
        return JsonResponse({'post': serialize_post(post, request.user, include_comments=True)})

    if request.method == 'DELETE':
        if post.author_id != request.user.id:
            return JsonResponse({'message': '본인이 작성한 게시글만 삭제할 수 있습니다.'}, status=403)
        post.delete()
        return JsonResponse({'message': '게시글을 삭제했습니다.'})

    return JsonResponse({'message': '지원하지 않는 요청입니다.'}, status=405)


@csrf_exempt
@login_required
def api_community_comments(request, post_id):
    post = CommunityPost.objects.filter(id=post_id).first()
    if post is None:
        return JsonResponse({'message': '게시글을 찾을 수 없습니다.'}, status=404)
    if request.method != 'POST':
        return JsonResponse({'message': 'POST 요청만 지원합니다.'}, status=405)
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'message': '댓글 내용을 입력해 주세요.'}, status=400)
    comment = CommunityComment.objects.create(post=post, author=request.user, content=content)
    return JsonResponse({'comment': serialize_comment(comment, request.user)}, status=201)


@csrf_exempt
@login_required
def api_community_comment_detail(request, comment_id):
    comment = CommunityComment.objects.select_related('post', 'author').filter(id=comment_id).first()
    if comment is None:
        return JsonResponse({'message': '댓글을 찾을 수 없습니다.'}, status=404)
    if comment.author_id != request.user.id:
        return JsonResponse({'message': '본인이 작성한 댓글만 수정/삭제할 수 있습니다.'}, status=403)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            return JsonResponse({'message': '댓글 내용을 입력해 주세요.'}, status=400)
        comment.content = content
        comment.save(update_fields=['content', 'updated_at'])
        return JsonResponse({'comment': serialize_comment(comment, request.user)})

    if request.method == 'DELETE':
        comment.delete()
        return JsonResponse({'message': '댓글을 삭제했습니다.'})

    return JsonResponse({'message': '지원하지 않는 요청입니다.'}, status=405)


def xlsx_column_index(cell_ref):
    letters = ''.join(char for char in cell_ref if char.isalpha())
    index = 0
    for char in letters:
        index = index * 26 + ord(char.upper()) - 64
    return index - 1


def parse_xlsx_date(value):
    if isinstance(value, str):
        value = value.strip()
    try:
        serial = int(float(value))
    except (TypeError, ValueError):
        return None
    return date(1899, 12, 30) + timedelta(days=serial)


def parse_decimal(value):
    if value is None:
        return None
    try:
        return Decimal(str(value).replace(',', '').strip())
    except (InvalidOperation, ValueError):
        return None


def get_shared_strings(zip_file):
    try:
        root = ET.fromstring(zip_file.read('xl/sharedStrings.xml'))
    except KeyError:
        return []
    strings = []
    for item in root.findall('a:si', XLSX_NS):
        texts = [text.text or '' for text in item.findall('.//a:t', XLSX_NS)]
        strings.append(''.join(texts))
    return strings


def get_first_sheet_path(zip_file):
    workbook = ET.fromstring(zip_file.read('xl/workbook.xml'))
    relationships = ET.fromstring(zip_file.read('xl/_rels/workbook.xml.rels'))
    relationship_map = {
        relationship.attrib['Id']: relationship.attrib['Target']
        for relationship in relationships
    }
    sheet = workbook.find('a:sheets/a:sheet', XLSX_NS)
    relation_id = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
    target = relationship_map[relation_id]
    return f"xl/{target.lstrip('/')}"


@lru_cache(maxsize=4)
def load_spot_price_file(asset):
    config = SPOT_PRICE_FILES[asset]
    path = config['path']
    if not path.exists():
        return []

    with ZipFile(path) as zip_file:
        shared_strings = get_shared_strings(zip_file)
        sheet = ET.fromstring(zip_file.read(get_first_sheet_path(zip_file)))
        rows = []
        for row in sheet.findall('.//a:sheetData/a:row', XLSX_NS):
            values = []
            for cell in row.findall('a:c', XLSX_NS):
                column_index = xlsx_column_index(cell.attrib.get('r', 'A'))
                while len(values) <= column_index:
                    values.append(None)
                value_node = cell.find('a:v', XLSX_NS)
                value = value_node.text if value_node is not None else ''
                if cell.attrib.get('t') == 's' and value:
                    value = shared_strings[int(value)]
                values[column_index] = value
            rows.append(values)

    if not rows:
        return []

    headers = [str(header).strip() if header is not None else '' for header in rows[0]]
    date_index = headers.index('Date') if 'Date' in headers else 0
    close_index = headers.index('Close/Last') if 'Close/Last' in headers else 1
    prices = []
    for row in rows[1:]:
        if len(row) <= max(date_index, close_index):
            continue
        price_date = parse_xlsx_date(row[date_index])
        close_price = parse_decimal(row[close_index])
        if price_date is None or close_price is None:
            continue
        prices.append({
            'date': price_date.isoformat(),
            'price': float(close_price),
        })
    return sorted(prices, key=lambda item: item['date'])


@login_required
def api_spot_prices(request):
    asset = request.GET.get('asset', 'gold').strip().lower()
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end', '').strip()
    if asset not in SPOT_PRICE_FILES:
        return JsonResponse({'message': '지원하지 않는 현물 자산입니다.'}, status=400)

    prices = load_spot_price_file(asset)
    if start:
        prices = [item for item in prices if item['date'] >= start]
    if end:
        prices = [item for item in prices if item['date'] <= end]

    return JsonResponse({
        'asset': asset,
        'asset_name': SPOT_PRICE_FILES[asset]['name'],
        'prices': prices,
    })


def serialize_subscription(subscription):
    product = subscription.product
    best_option = (
        product.options.order_by('-max_interest_rate', '-interest_rate', 'saving_term')
        .first()
    )
    rate = None
    if best_option:
        rate = best_option.max_interest_rate or best_option.interest_rate
    return {
        'id': subscription.id,
        'product_id': product.id,
        'product_name': product.product_name,
        'financial_company_name': product.financial_company_name,
        'product_type': product.get_product_type_display(),
        'best_term': best_option.saving_term if best_option else None,
        'rate': float(rate) if rate is not None else 0,
        'rate_label': f'{rate}%' if rate is not None else '-',
        'created_at': timezone.localtime(subscription.created_at).strftime('%Y-%m-%d'),
    }


def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


@csrf_exempt
@login_required
def api_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        birth_date_value = request.POST.get('birth_date', '').strip()

        if not name or not email:
            return JsonResponse({'message': '이름과 이메일을 입력해 주세요.'}, status=400)
        if User.objects.exclude(id=request.user.id).filter(username=email).exists() or User.objects.exclude(id=request.user.id).filter(email=email).exists():
            return JsonResponse({'message': '이미 사용 중인 이메일입니다.'}, status=400)

        birth_date = None
        age = None
        if birth_date_value:
            try:
                birth_date = datetime.strptime(birth_date_value, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'message': '생년월일 형식이 올바르지 않습니다.'}, status=400)
            age = calculate_age(birth_date)

        request.user.first_name = name
        request.user.email = email
        request.user.username = email
        request.user.save(update_fields=['first_name', 'email', 'username'])
        profile.birth_date = birth_date
        profile.age = age
        profile.save(update_fields=['birth_date', 'age'])

    subscriptions = (
        UserDepositSubscription.objects
        .filter(user=request.user)
        .select_related('product')
        .prefetch_related('product__options')
    )
    subscription_list = [serialize_subscription(subscription) for subscription in subscriptions]
    return JsonResponse({
        'profile': {
            'name': request.user.first_name or request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'birth_date': profile.birth_date.isoformat() if profile.birth_date else '',
            'age': profile.age,
            'joined_at': timezone.localtime(request.user.date_joined).strftime('%Y-%m-%d'),
        },
        'subscriptions': subscription_list,
        'chart': {
            'labels': [item['product_name'] for item in subscription_list],
            'rates': [item['rate'] for item in subscription_list],
        },
    })


def serialize_deposit_product(product, user=None):
    best_option = (
        product.options.order_by('-max_interest_rate', '-interest_rate', 'saving_term')
        .first()
    )
    is_favorite = (
        bool(user and user.is_authenticated)
        and UserFavoriteDepositProduct.objects.filter(user=user, product=product).exists()
    )
    return {
        'id': product.id,
        'product_type': product.product_type,
        'product_type_display': product.get_product_type_display(),
        'financial_company_name': product.financial_company_name,
        'product_name': product.product_name,
        'join_way': product.join_way,
        'max_limit': product.max_limit,
        'best_term': best_option.saving_term if best_option else None,
        'interest_rate': str(best_option.interest_rate) if best_option and best_option.interest_rate is not None else None,
        'max_interest_rate': str(best_option.max_interest_rate) if best_option and best_option.max_interest_rate is not None else None,
        'is_favorite': is_favorite,
    }


def api_deposit_products(request):
    products = DepositProduct.objects.prefetch_related('options').all()

    company = request.GET.get('company', '').strip()
    keyword = request.GET.get('q', '').strip()
    kind = request.GET.get('kind', '').strip()
    ordering = request.GET.get('ordering', 'rate').strip()

    if company:
        products = products.filter(financial_company_name=company)
    if keyword:
        products = products.filter(product_name__icontains=keyword)
    if kind in ['deposit', 'saving']:
        products = products.filter(product_type=kind)

    product_list = [serialize_deposit_product(product, request.user) for product in products]
    if ordering == 'name':
        product_list.sort(key=lambda item: item['product_name'])
    elif ordering == 'company':
        product_list.sort(key=lambda item: (item['financial_company_name'], item['product_name']))
    else:
        product_list.sort(
            key=lambda item: float(item['max_interest_rate'] or item['interest_rate'] or 0),
            reverse=True,
        )

    companies = list(
        DepositProduct.objects
        .order_by('financial_company_name')
        .values_list('financial_company_name', flat=True)
        .distinct()
    )
    return JsonResponse({'products': product_list, 'companies': companies})


def parse_stock_number(value, default=0):
    if value in [None, '']:
        return default
    try:
        return Decimal(str(value).replace(',', ''))
    except (InvalidOperation, ValueError):
        return default


def serialize_stock_item(item):
    current_price = parse_stock_number(item.get('clpr'))
    change = parse_stock_number(item.get('vs'))
    change_rate = parse_stock_number(item.get('fltRt'))
    volume = parse_stock_number(item.get('trqu'))
    market_cap = parse_stock_number(item.get('mrktTotAmt'))

    return {
        'code': item.get('srtnCd') or item.get('isinCd') or '',
        'isin_code': item.get('isinCd') or '',
        'name': item.get('itmsNm') or '',
        'market': item.get('mrktCtg') or '',
        'base_date': item.get('basDt') or '',
        'current_price': int(current_price),
        'change': int(change),
        'change_rate': float(change_rate),
        'volume': int(volume),
        'market_cap': int(market_cap),
    }


DEFAULT_STOCK_MARKETS = ['KOSPI', 'KOSDAQ', 'KONEX']


def api_stocks(request):
    api_key = unquote(settings.KRX_API_KEY)

    if not api_key:
        return JsonResponse(
            {"message": "공공데이터포털 API 키가 설정되어 있지 않습니다."},
            status=500
        )

    keyword = request.GET.get("q", "").strip()
    market = request.GET.get("market", "").strip()
    ordering = request.GET.get("ordering", "market_cap").strip()
    try:
        page = max(int(request.GET.get("page", "1") or 1), 1)
    except ValueError:
        page = 1
    try:
        per_page = min(max(int(request.GET.get("per_page", "30") or 30), 1), 100)
    except ValueError:
        per_page = 30

    fetch_count = 500 if keyword else 3000

    params = {
        "serviceKey": api_key,
        "resultType": "json",
        "pageNo": "1",
        "numOfRows": str(fetch_count),
    }

    if keyword:
        if keyword.isdigit():
            params["likeSrtnCd"] = keyword
        else:
            params["likeItmsNm"] = keyword

    try:
        response = requests.get(
            settings.STOCK_API_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()
        payload = response.json()

    except requests.RequestException:
        return JsonResponse(
            {"message": "주식 API 요청에 실패했습니다."},
            status=502
        )

    except ValueError:
        return JsonResponse(
            {
                "message": "주식 API 응답이 JSON 형식이 아닙니다.",
            },
            status=502
        )

    body = payload.get("response", {}).get("body", {})
    items = body.get("items", {}).get("item", [])

    if isinstance(items, dict):
        items = [items]

    stocks = [serialize_stock_item(item) for item in items]
    stocks = deduplicate_latest_stocks(stocks)
    markets = sorted({
        *DEFAULT_STOCK_MARKETS,
        *(stock["market"] for stock in stocks if stock["market"]),
    })

    if market:
        stocks = [stock for stock in stocks if stock["market"] == market]

    if ordering == "name":
        stocks.sort(key=lambda item: item["name"])
    elif ordering == "price":
        stocks.sort(key=lambda item: item["current_price"], reverse=True)
    elif ordering == "change_rate":
        stocks.sort(key=lambda item: item["change_rate"], reverse=True)
    else:
        stocks.sort(key=lambda item: item["market_cap"], reverse=True)

    total_count = len(stocks)
    start = (page - 1) * per_page
    end = start + per_page

    return JsonResponse({
        "stocks": stocks[start:end],
        "markets": markets,
        "total_count": total_count,
    })


def api_deposit_product_detail(request, product_id):
    product = DepositProduct.objects.prefetch_related('options').filter(id=product_id).first()
    if product is None:
        return JsonResponse({'message': '상품을 찾을 수 없습니다.'}, status=404)
    is_subscribed = (
        request.user.is_authenticated
        and UserDepositSubscription.objects.filter(user=request.user, product=product).exists()
    )

    return JsonResponse({
        'product': {
            **serialize_deposit_product(product, request.user),
            'is_subscribed': is_subscribed,
            'product_code': product.product_code,
            'disclosure_month': product.disclosure_month,
            'maturity_interest': product.maturity_interest,
            'special_condition': product.special_condition,
            'join_member': product.join_member,
            'etc_note': product.etc_note,
            'options': [
                {
                    'saving_term': option.saving_term,
                    'interest_rate_type_name': option.interest_rate_type_name,
                    'reserve_type_name': option.reserve_type_name,
                    'interest_rate': str(option.interest_rate) if option.interest_rate is not None else None,
                    'max_interest_rate': str(option.max_interest_rate) if option.max_interest_rate is not None else None,
                }
                for option in product.options.all()
            ],
        }
    })


@login_required
def api_favorite_deposit_products(request):
    favorites = (
        UserFavoriteDepositProduct.objects
        .filter(user=request.user)
        .select_related('product')
        .prefetch_related('product__options')
    )
    return JsonResponse({
        'products': [
            serialize_deposit_product(favorite.product, request.user)
            for favorite in favorites
        ]
    })


@csrf_exempt
@login_required
def api_favorite_deposit_product_toggle(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'message': 'POST 요청만 지원합니다.'}, status=405)
    product = DepositProduct.objects.filter(id=product_id).first()
    if product is None:
        return JsonResponse({'message': '상품을 찾을 수 없습니다.'}, status=404)

    favorite = UserFavoriteDepositProduct.objects.filter(user=request.user, product=product).first()
    if favorite:
        favorite.delete()
        is_favorite = False
        message = '관심상품에서 제거했습니다.'
    else:
        UserFavoriteDepositProduct.objects.create(user=request.user, product=product)
        is_favorite = True
        message = '관심상품에 추가했습니다.'

    return JsonResponse({
        'message': message,
        'is_favorite': is_favorite,
        'product': serialize_deposit_product(product, request.user),
    })


@login_required
def api_bank_route(request):
    destination_lng = request.GET.get('lng', '').strip()
    destination_lat = request.GET.get('lat', '').strip()
    if not destination_lng or not destination_lat:
        return JsonResponse({'message': '목적지 좌표가 필요합니다.'}, status=400)
    if not settings.KAKAO_MOBILITY_REST_KEY:
        return JsonResponse({'message': '.env에 KAKAO_MOBILITY_REST_KEY를 설정해 주세요.'}, status=400)

    try:
        response = requests.get(
            'https://apis-navi.kakaomobility.com/v1/directions',
            headers={'Authorization': f'KakaoAK {settings.KAKAO_MOBILITY_REST_KEY}'},
            params={
                'origin': '127.039585,37.5012743',
                'destination': f'{destination_lng},{destination_lat}',
                'priority': 'RECOMMEND',
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        return JsonResponse({'message': f'경로 API 요청에 실패했습니다: {exc}'}, status=502)

    routes = data.get('routes') or []
    if not routes:
        return JsonResponse({'message': '경로를 찾지 못했습니다.'}, status=404)

    route = routes[0]
    points = []
    for section in route.get('sections', []):
        for road in section.get('roads', []):
            vertexes = road.get('vertexes', [])
            for index in range(0, len(vertexes), 2):
                points.append({
                    'lng': vertexes[index],
                    'lat': vertexes[index + 1],
                })

    summary = route.get('summary', {})
    return JsonResponse({
        'distance': summary.get('distance'),
        'duration': summary.get('duration'),
        'points': points,
    })


@login_required
def api_map_config(request):
    return JsonResponse({
        'kakao_map_app_key': settings.KAKAO_MAP_APP_KEY,
    })


@csrf_exempt
@login_required
def api_join_deposit_product(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'message': 'POST 요청만 지원합니다.'}, status=405)

    product = DepositProduct.objects.filter(id=product_id).first()
    if product is None:
        return JsonResponse({'message': '상품을 찾을 수 없습니다.'}, status=404)

    subscription, created = UserDepositSubscription.objects.get_or_create(
        user=request.user,
        product=product,
    )
    return JsonResponse({
        'message': '가입 목록에 추가했습니다.' if created else '이미 가입 목록에 있는 상품입니다.',
        'is_subscribed': True,
        'subscription_id': subscription.id,
    })



from django.http import JsonResponse

def test_api(request):
    return JsonResponse({
        "message": "Django API 연결 성공",
        "project": "FinPick"
    })



from django.http import JsonResponse
from .models import DepositProduct


def deposit_product_list_api(request):
    products = DepositProduct.objects.all()

    data = []

    for product in products:
        data.append({
            "id": product.id,
            "product_type": product.product_type,
            "product_type_display": product.get_product_type_display(),
            "disclosure_month": product.disclosure_month,
            "financial_company_code": product.financial_company_code,
            "financial_company_name": product.financial_company_name,
            "product_code": product.product_code,
            "product_name": product.product_name,
            "join_way": product.join_way,
            "maturity_interest": product.maturity_interest,
            "special_condition": product.special_condition,
            "join_deny": product.join_deny,
            "join_member": product.join_member,
            "etc_note": product.etc_note,
            "max_limit": product.max_limit,
            "updated_at": product.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return JsonResponse(data, safe=False)


from django.http import JsonResponse
from .models import DepositProduct


def deposit_product_list_api(request):
    products = DepositProduct.objects.all()

    data = []

    for product in products:
        data.append({
            "id": product.id,
            "product_type": product.product_type,
            "product_type_display": product.get_product_type_display(),
            "disclosure_month": product.disclosure_month,
            "financial_company_code": product.financial_company_code,
            "financial_company_name": product.financial_company_name,
            "product_code": product.product_code,
            "product_name": product.product_name,
            "join_way": product.join_way,
            "maturity_interest": product.maturity_interest,
            "special_condition": product.special_condition,
            "join_deny": product.join_deny,
            "join_member": product.join_member,
            "etc_note": product.etc_note,
            "max_limit": product.max_limit,
            "updated_at": product.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def signup_api(request):
    if request.method != "POST":
        return JsonResponse({
            "message": "POST 요청만 허용됩니다."
        }, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "message": "잘못된 요청 형식입니다."
        }, status=400)

    username = body.get("username")
    email = body.get("email")
    name = body.get("name")
    birth_date_value = body.get("birth_date")
    password1 = body.get("password1")
    password2 = body.get("password2")

    if not username or not email or not name or not birth_date_value or not password1 or not password2:
        return JsonResponse({
            "message": "모든 항목을 입력해주세요."
        }, status=400)

    try:
        birth_date = datetime.strptime(birth_date_value, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({
            "message": "?앸뀈?붿씪 ?뺤떇???щ컮瑜댁? ?딆뒿?덈떎."
        }, status=400)

    age = calculate_age(birth_date)

    if password1 != password2:
        return JsonResponse({
            "message": "비밀번호가 일치하지 않습니다."
        }, status=400)

    User = get_user_model()

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "message": "이미 사용 중인 아이디입니다."
        }, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({
            "message": "이미 가입된 이메일입니다."
        }, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password1,
        first_name=name,
    )
    UserProfile.objects.create(user=user, birth_date=birth_date, age=age)

    return JsonResponse({
        "message": "회원가입이 완료되었습니다.",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.first_name,
            "birth_date": birth_date.isoformat(),
            "age": age,
        }
    }, status=201)


@csrf_exempt
def login_api(request):
    if request.method != "POST":
        return JsonResponse({
            "message": "POST 요청만 허용됩니다."
        }, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "message": "잘못된 요청 형식입니다."
        }, status=400)

    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        return JsonResponse({
            "message": "아이디와 비밀번호를 입력해주세요."
        }, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({
            "message": "아이디 또는 비밀번호가 올바르지 않습니다."
        }, status=400)

    login(request, user)

    return JsonResponse({
        "message": "로그인되었습니다.",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.first_name,
        }
    })


def session_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "authenticated": False,
            "user": None,
        })

    return JsonResponse({
        "authenticated": True,
        "user": {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "name": request.user.first_name,
        },
    })


@csrf_exempt
def logout_api(request):
    if request.method != "POST":
        return JsonResponse({
            "message": "POST ?붿껌留??덉슜?⑸땲??"
        }, status=405)

    logout(request)
    return JsonResponse({
        "message": "濡쒓렇?꾩썐?섏뿀?듬땲??",
        "authenticated": False,
    })


def dashboard_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "message": "로그인이 필요합니다."
        }, status=401)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.birth_date:
        current_age = calculate_age(profile.birth_date)
        if profile.age != current_age:
            profile.age = current_age
            profile.save(update_fields=["age"])

    data = {
        "user": {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "name": request.user.first_name,
        },
        "profile": {
            "age": profile.age,
            "job": profile.job,
            "monthly_income": profile.monthly_income,
            "monthly_expense": profile.monthly_expense,
            "residence_type": profile.residence_type,
            "saving_status": profile.saving_status,
            "invest_experience": profile.invest_experience,
            "birth_date": profile.birth_date.isoformat() if profile.birth_date else "",
            "created_at": profile.created_at.strftime("%Y-%m-%d") if profile.created_at else "",
        }
    }

    return JsonResponse(data)

@csrf_exempt
def diagnosis_api(request):
    if request.method != "POST":
        return JsonResponse({
            "message": "POST 요청만 허용됩니다."
        }, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({
            "message": "로그인이 필요합니다."
        }, status=401)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "message": "잘못된 요청 형식입니다."
        }, status=400)

    income_level = body.get("income_level")
    spending_style = body.get("spending_style")
    financial_goal = body.get("financial_goal")
    investment_style = body.get("investment_style")
    asset_level = body.get("asset_level")
    loan_type = body.get("loan_type")

    if not all([
        income_level,
        spending_style,
        financial_goal,
        investment_style,
        asset_level,
        loan_type,
    ]):
        return JsonResponse({
            "message": "모든 문항에 답변해주세요."
        }, status=400)

    result = {
        "financial_type": "금융 기초형",
        "intro": "금융 습관을 차근차근 만들어가면 좋은 단계입니다.",
        "readiness_score": 60,
        "profile_scores": {
            "저축 습관": "★★★☆☆",
            "소비 관리": "★★★☆☆",
            "투자 성향": "★★☆☆☆",
            "자산 관리": "★★★☆☆",
        },
        "strengths": [
            "금융 목표를 가지고 있습니다.",
            "자신의 소비 성향을 인식하고 있습니다.",
        ],
        "improvements": [
            "비상금 마련이 필요합니다.",
            "투자 전 기초 금융 지식을 쌓는 것이 좋습니다.",
        ],
        "finpick_comment": "지금은 무리한 투자보다 저축 습관과 비상금 마련이 우선입니다.",
    }

    return JsonResponse({
        "message": "진단이 완료되었습니다.",
        "result": result,
    }, status=201)

def deduplicate_latest_stocks(stocks):
    latest_by_code = {}

    for stock in stocks:
        code = stock.get("code")
        base_date = stock.get("base_date", "")

        if not code:
            continue

        if code not in latest_by_code:
            latest_by_code[code] = stock
        else:
            existing_date = latest_by_code[code].get("base_date", "")
            if base_date > existing_date:
                latest_by_code[code] = stock

    return list(latest_by_code.values())
