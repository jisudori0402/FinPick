from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import DiagnosisResult, ProductRecommendation, RoadmapStep, UserProfile


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    roadmap = list(RoadmapStep.objects.values('step_number', 'title', 'description'))
    products = list(ProductRecommendation.objects.values('name', 'product_type', 'reason', 'category'))
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
    })


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1 or not password2:
            messages.error(request, '필수 항목을 모두 입력해 주세요.')
            return render(request, 'signup.html')
        if password1 != password2:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 사용 중인 아이디입니다.')
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.create(user=user)
        login(request, user)
        messages.success(request, '회원가입이 완료되었습니다.')
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


@csrf_exempt
@login_required
def api_diagnosis(request):
    if request.method == 'POST':
        data = request.POST
        result = DiagnosisResult.objects.create(
            user=request.user,
            income=data.get('income', '0'),
            expense=data.get('expense', '0'),
            saving=data.get('saving', '0'),
            invest=data.get('invest', '없음'),
        )
        return JsonResponse({
            'id': result.id,
            'level': 'Lv.1 금융 새싹 🌱',
            'summary': '현재는 투자보다 비상금과 저축 습관 형성이 우선입니다.',
            'checks': [
                '비상금 부족',
                '저축 습관 형성 필요',
                '금융상품 우선순위 설정 필요',
            ],
        })
    return JsonResponse({'message': 'POST 요청만 지원합니다.'}, status=405)


def api_roadmap(request):
    steps = list(RoadmapStep.objects.values('step_number', 'title', 'description'))
    return JsonResponse({'roadmap': steps})


def api_products(request):
    products = list(ProductRecommendation.objects.values('name', 'product_type', 'reason', 'category'))
    return JsonResponse({'products': products})
