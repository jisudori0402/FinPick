# FinPick 배포 가이드

이 프로젝트는 Render 기준으로 백엔드(Django), 프론트엔드(Vue 정적 사이트), PostgreSQL DB를 분리 배포할 수 있도록 `render.yaml`을 포함합니다.

## 1. 사전 준비

- GitHub 저장소에 현재 코드를 push합니다.
- Render 계정에서 GitHub 저장소 접근 권한을 연결합니다.
- `.env`의 실제 키 값은 저장소에 올리지 말고 Render 환경변수에 등록합니다.

## 2. Render Blueprint 배포

1. Render Dashboard에서 **New +**를 선택합니다.
2. **Blueprint**를 선택합니다.
3. FinPick GitHub 저장소를 연결합니다.
4. 루트의 `render.yaml`을 기준으로 서비스를 생성합니다.
5. 생성되는 서비스는 다음과 같습니다.
   - `finpick-backend`: Django API 서버
   - `finpick-frontend`: Vue 정적 사이트
   - `finpick-db`: PostgreSQL DB

## 3. 백엔드 환경변수

`finpick-backend`에 다음 값을 등록합니다.

```env
DEBUG=False
IS_PRODUCTION=True
ALLOWED_HOSTS=백엔드서비스.onrender.com
CORS_ALLOWED_ORIGINS=https://프론트엔드서비스.onrender.com
CSRF_TRUSTED_ORIGINS=https://프론트엔드서비스.onrender.com
DATABASE_URL=Render PostgreSQL 연결 문자열
KAKAO_MAP_APP_KEY=
KAKAO_MOBILITY_REST_KEY=
YOUTUBE_DATA_API_KEY=
KRX_API_KEY=
GMS_API_KEY=
GMS_OPENAI_BASE_URL=
GMS_OPENAI_MODEL=gpt-4.1-mini
LOGO_DEV_KEY=
FINLIFE_API_KEY=
```

`SECRET_KEY`와 `DATABASE_URL`은 `render.yaml`에서 자동 생성 또는 DB 연결값으로 주입되도록 설정되어 있습니다.

## 4. 프론트엔드 환경변수

`finpick-frontend`에 다음 값을 등록합니다.

```env
VITE_API_BASE_URL=https://백엔드서비스.onrender.com
```

프론트엔드는 빌드 시점에 이 값을 사용하므로, 값을 수정하면 프론트 서비스를 다시 배포해야 합니다.

## 5. 빌드 명령

백엔드:

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

백엔드 시작 명령:

```bash
gunicorn finpick_project.wsgi:application
```

프론트엔드:

```bash
npm install
npm run build
```

정적 배포 경로:

```text
frontend/dist
```

## 6. 배포 후 확인

- 백엔드 `/api/test/`가 응답하는지 확인합니다.
- 프론트엔드에서 회원가입/로그인이 되는지 확인합니다.
- 로그인 후 금융 진단, 로드맵, 상품 조회가 동작하는지 확인합니다.
- 세션이 유지되지 않으면 `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, `VITE_API_BASE_URL` 값을 다시 확인합니다.

