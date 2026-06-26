import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
load_dotenv(BASE_DIR.parent / '.env')

SECRET_KEY = os.environ.get("SECRET_KEY", "local-dev-secret-key")

DEBUG = os.environ.get("DEBUG", "False") == "True"

def csv_env(name, default=""):
    return [value.strip() for value in os.environ.get(name, default).split(",") if value.strip()]


ALLOWED_HOSTS = csv_env("ALLOWED_HOSTS", "localhost,127.0.0.1")

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'finpick_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'finpick_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'finpick_project.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
LOGIN_URL = 'login'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
KAKAO_MAP_APP_KEY = os.getenv('KAKAO_MAP_APP_KEY', '')
KAKAO_MOBILITY_REST_KEY = os.getenv('KAKAO_MOBILITY_REST_KEY', '')
YOUTUBE_DATA_API_KEY = os.getenv('YOUTUBE_DATA_API_KEY', '')
KRX_API_KEY = os.getenv('KRX_API_KEY') or os.getenv('STOCK_API_KEY') or os.getenv('DATA_GO_KR_API_KEY', '')
STOCK_API_URL = os.getenv(
    'STOCK_API_URL',
    'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo',
)
GMS_API_KEY = os.getenv('GMS_API_KEY', '')
GMS_OPENAI_BASE_URL = (
    os.getenv('GMS_OPENAI_BASE_URL')
    or os.getenv('GMS_BASE_URL')
    or ''
)
GMS_OPENAI_MODEL = os.getenv('GMS_OPENAI_MODEL', 'gpt-4.1-mini')
LOGO_DEV_KEY = os.getenv("LOGO_DEV_KEY", "")

CORS_ALLOWED_ORIGINS = csv_env(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173",
)

CSRF_TRUSTED_ORIGINS = csv_env(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:5173",
)

CORS_ALLOW_CREDENTIALS = True

IS_PRODUCTION = os.environ.get("IS_PRODUCTION", "False") == "True"

SESSION_COOKIE_SAMESITE = "None" if IS_PRODUCTION else "Lax"
SESSION_COOKIE_SECURE = IS_PRODUCTION

CSRF_COOKIE_SAMESITE = "None" if IS_PRODUCTION else "Lax"
CSRF_COOKIE_SECURE = IS_PRODUCTION
