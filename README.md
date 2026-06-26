# FinPick

> 사회초년생을 위한 금융 진단, 로드맵, 맞춤형 상품 추천 서비스

FinPick은 금융 관리가 익숙하지 않은 사회초년생이 자신의 금융 상태를 진단하고, 단계별 성장 로드맵과 예금/적금 및 주식 정보를 함께 확인할 수 있도록 만든 Django + Vue 기반 금융 서비스입니다.

사용자는 소득, 지출, 금융 목표, 투자 성향, 자산 수준, 대출 상태 등을 입력해 금융 준비도를 확인합니다. FinPick은 진단 결과를 바탕으로 금융 점수, 금융 유형, 강점과 보완점, 오늘의 금융 메시지, 단계별 미션 로드맵, 맞춤형 금융상품 추천을 제공합니다.

단순히 상품 목록을 나열하는 서비스가 아니라, 사용자의 현재 상태를 먼저 해석한 뒤 다음 행동으로 이어지도록 돕는 개인화 서비스입니다.

## 기획 배경

사회초년생은 금융 정보는 많이 접하지만, 자신의 상황에 맞는 선택 기준을 세우기 어렵습니다. 예금, 적금, 투자, 비상금, 소비 관리 같은 주제는 서로 연결되어 있는데 실제 서비스에서는 상품 비교와 금융 교육이 분리되어 있는 경우가 많습니다.

FinPick은 사용자의 소득, 지출, 대출 가능 금액, 비상금, 투자 경험 등을 기준으로 금융 상태를 진단하고, 그 결과를 로드맵과 상품 추천까지 연결합니다. 이를 통해 사용자는 "지금 어떤 상품을 볼 것인가"뿐 아니라 "왜 이 상품이 나에게 맞는가"와 "다음에 무엇을 해야 하는가"를 함께 확인할 수 있습니다.

## 주요 기능

### 회원가입 및 로그인

- Django 기본 User 모델과 세션 기반 인증을 사용합니다.
- Vue Router의 라우트 가드를 통해 로그인 상태에 따라 접근 가능한 화면을 분기합니다.
- 회원가입 시 이름, 이메일, 생년월일, 비밀번호를 입력하고 `UserProfile`을 생성합니다.
- 로그인, 로그아웃, 세션 확인, 비밀번호 변경, 비밀번호 재설정 API가 구현되어 있습니다.
- 프로필 화면에서는 직업, 월 소득, 월 지출, 거주 형태, 저축 상태, 투자 경험, 자기소개, 프로필 이미지를 관리할 수 있습니다.

### 금융 진단

- 사용자는 소득 수준, 소비 성향, 금융 목표, 투자 성향, 자산 수준, 대출 상태를 입력합니다.
- 백엔드는 입력값을 바탕으로 저축 점수, 소비 점수, 투자 점수, 안정성 점수를 계산합니다.
- 진단 결과로 금융 유형, 준비도 점수, 강점, 보완점, FinPick 코멘트, 프로필별 점수를 저장합니다.
- 로그인 사용자는 최신 진단 결과를 조회할 수 있습니다.

### AI 기반 진단 결과 분석

- 진단 결과를 바탕으로 강점, 보완점, 오늘의 금융 메시지를 생성합니다.
- `FinancialGuide` 데이터를 검색해 진단 결과와 관련 있는 금융 가이드 내용을 프롬프트에 함께 전달하는 RAG 확장 구조가 포함되어 있습니다.
- 추천 상품은 AI가 임의로 고르는 방식이 아니라, 백엔드에서 진단 결과와 상품 속성을 기준으로 먼저 점수화한 뒤 AI가 추천 이유를 설명하는 구조입니다.
- 과장된 투자 권유를 피하고 사회초년생이 이해하기 쉬운 문장으로 응답하도록 프롬프트를 제한합니다.

### 금융 성장 로드맵

- 진단 결과의 금융 유형에 따라 단계별 로드맵을 생성합니다.
- 각 단계에는 사용자가 수행할 수 있는 미션이 포함됩니다.
- 사용자는 미션 완료 여부를 토글할 수 있고, 완료 시각이 저장됩니다.
- 대시보드와 로드맵 화면에서 다음 추천 행동을 확인할 수 있습니다.

### 예금/적금 상품 추천 및 조회

- 금융감독원 금융상품통합비교공시 API를 통해 예금/적금 상품과 옵션 데이터를 동기화할 수 있습니다.
- 상품 목록에서는 은행명, 상품명, 가입 방법, 가입 기간, 금리, 우대 조건 등을 확인할 수 있습니다.
- 상품 상세 화면에서는 옵션, 금리, 가입 제한, 유의사항을 확인할 수 있습니다.
- 사용자는 예금/적금 상품을 관심 상품으로 저장하거나 가입 관심 목록에 추가할 수 있습니다.
- 진단 결과와 사용자 프로필을 바탕으로 예금/적금 추천 점수를 계산하고, AI가 추천 이유를 보완 설명합니다.

### 주식 정보 조회

- 공공데이터포털 주식 API를 기반으로 국내 주식 정보를 조회합니다.
- 종목명, 시장, 현재가, 등락, 등락률, 거래량, 시가총액 등을 제공합니다.
- 종목 상세 화면과 관심 주식 토글 기능이 구현되어 있습니다.
- `logo.dev` 키가 설정되어 있으면 일부 종목에 대해 회사 로고 URL을 생성합니다. 키가 없거나 매핑이 없는 종목은 기본 로고 또는 로고 없음 상태로 처리됩니다.

### 지도 및 은행 찾기

- Kakao Map JavaScript 키와 Kakao Mobility REST 키를 사용해 은행 위치 및 경로 관련 API를 제공합니다.
- 프론트엔드에는 예금/적금 상품 상세에서 은행 찾기 화면으로 이동하는 구조가 있습니다.

### 커뮤니티 및 금융 콘텐츠

- 커뮤니티 게시글 작성, 조회, 수정, 삭제 기능이 구현되어 있습니다.
- 게시글 댓글 작성, 조회, 수정, 삭제 기능이 구현되어 있습니다.
- YouTube Data API를 이용해 금융 관련 영상을 검색하고 상세 정보를 조회할 수 있습니다.
- 검색 키워드는 `SearchKeywordTrend`에 저장되어 인기 검색어로 활용됩니다.

### 아직 미구현 또는 확장 예정 기능

- 카드 상품 전용 모델과 API는 현재 코드에 별도로 구현되어 있지 않습니다.
- 벡터 DB 기반 RAG 검색은 아직 적용되어 있지 않고, 현재는 DB의 `FinancialGuide`를 키워드 기반으로 검색해 프롬프트에 포함하는 구조입니다.
- 커뮤니티 좋아요, 북마크, 신고 기능은 향후 확장 대상으로 볼 수 있습니다.

## 기술 스택

### Backend

- Python
- Django 5
- Django JsonResponse 기반 API
- django-cors-headers
- SQLite
- python-dotenv
- requests
- OpenAI Python SDK

### Frontend

- Vue 3
- Vite
- Vue Router
- Pinia
- Axios
- CSS

### AI

- OpenAI 호환 Chat Completions API
- `GMS_API_KEY`, `GMS_OPENAI_BASE_URL`, `GMS_OPENAI_MODEL` 설정 기반 호출
- 금융 진단 결과 기반 개인화 문장 생성
- `FinancialGuide` 검색 결과를 프롬프트에 포함하는 RAG 확장 구조
- 백엔드 점수화 기반 추천 상품에 대한 AI 추천 이유 생성

### External API

- 금융감독원 금융상품통합비교공시 API
- 공공데이터포털 국내 주식 API
- YouTube Data API
- Kakao Map API
- Kakao Mobility API
- logo.dev 이미지 API

### Tools

- Git
- GitHub
- VSCode
- Postman

## 프로젝트 구조

```text
FinPick/
├─ backend/
│  ├─ manage.py
│  ├─ requirements.txt
│  ├─ templates/
│  │  ├─ dashboard.html
│  │  ├─ index.html
│  │  ├─ login.html
│  │  └─ signup.html
│  ├─ finpick_project/
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  ├─ asgi.py
│  │  └─ wsgi.py
│  └─ finpick_app/
│     ├─ models.py
│     ├─ views.py
│     ├─ urls.py
│     ├─ ai_services.py
│     ├─ product_recommendation_service.py
│     ├─ admin.py
│     ├─ migrations/
│     └─ management/
│        └─ commands/
│           ├─ seed_finpick.py
│           └─ sync_deposit_products.py
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.js
│  ├─ index.html
│  ├─ public/
│  │  ├─ bank_logos/
│  │  ├─ financial-types/
│  │  └─ product_category_icons/
│  └─ src/
│     ├─ App.vue
│     ├─ main.js
│     ├─ router/
│     │  └─ index.js
│     ├─ services/
│     │  └─ auth.js
│     ├─ assets/
│     ├─ components/
│     └─ views/
│        ├─ Homeview.vue
│        ├─ SignupView.vue
│        ├─ LoginView.vue
│        ├─ DashboardView.vue
│        ├─ DiagnosisView.vue
│        ├─ DiagnosisResultView.vue
│        ├─ RoadmapView.vue
│        ├─ DepositProductListView.vue
│        ├─ DepositProductDetailView.vue
│        ├─ StockProductDetailView.vue
│        ├─ BankSearchView.vue
│        ├─ CommunityView.vue
│        ├─ CommunityVideoDetailView.vue
│        ├─ PasswordChangeView.vue
│        └─ PasswordResetView.vue
├─ .gitignore
├─ package-lock.json
└─ README.md
```

## 주요 데이터 모델

### Django 기본 User

로그인 계정의 기본 정보를 저장합니다. `UserProfile`, `DiagnosisResult`, 로드맵 미션, 관심 상품, 커뮤니티 게시글과 연결됩니다.

### UserProfile

사용자 프로필 모델입니다. 생년월일, 나이, 직업, 월 소득, 월 지출, 거주 형태, 저축 상태, 투자 경험, 자기소개, 프로필 이미지, 비밀번호 변경일을 저장합니다.

### DiagnosisResult

금융 진단 결과를 저장합니다. 소득 수준, 소비 성향, 금융 목표, 투자 성향, 자산 수준, 대출 상태, 금융 유형, 준비도 점수, 강점, 보완점, FinPick 코멘트, 영역별 점수, 생성일을 관리합니다.

### RoadmapStep

초기 로드맵 단계 데이터를 저장하는 단순 로드맵 모델입니다. `seed_finpick` 명령에서 기본 데이터를 생성합니다.

### RoadmapTemplate

금융 유형과 레벨별 로드맵 템플릿입니다. 유형과 단계에 따라 사용자에게 보여줄 로드맵의 기준이 됩니다.

### RoadmapMission

로드맵 단계에 속한 개별 미션입니다. 미션 제목, 설명, 카테고리, 정렬 순서를 저장합니다.

### UserMission

사용자별 미션 완료 상태를 저장합니다. 특정 사용자가 어떤 미션을 완료했는지와 완료 시각을 관리합니다.

### ProductRecommendation

초기 추천 상품 데이터를 저장하는 모델입니다. 현재는 시드 데이터 기반의 단순 추천 항목으로 사용됩니다.

### DepositProduct

예금/적금 상품의 기본 정보를 저장합니다. 금융회사명, 상품명, 가입 방법, 만기 후 이자율, 우대 조건, 가입 대상, 한도, 원본 API 데이터를 관리합니다.

### DepositOption

예금/적금 상품의 금리 옵션을 저장합니다. 가입 기간, 금리 유형, 기본 금리, 최고 우대 금리, 적립 유형 등을 관리합니다.

### UserDepositSubscription

사용자가 가입 관심 목록에 추가한 예금/적금 상품을 저장합니다.

### UserFavoriteDepositProduct

사용자가 즐겨찾기한 예금/적금 상품을 저장합니다.

### UserFavoriteStock

사용자가 관심 등록한 주식 종목을 저장합니다. 종목 코드, 종목명, 시장, 현재가, 등락률, 거래량, 시가총액 등을 함께 저장합니다.

### DailyFinancialTip

AI가 생성한 오늘의 금융 메시지를 날짜별로 캐싱합니다.

### AiProductRecommendation

금융 유형별 AI 추천 결과를 날짜 단위로 캐싱합니다. 추천 예금/적금 상품 ID와 주식 코드를 JSON으로 저장합니다.

### FinancialGuide

AI/RAG 보조에 사용하는 금융 가이드 데이터입니다. 카테고리, 제목, 본문, 키워드를 저장하고 진단 결과와 관련된 가이드 검색에 사용합니다.

### SearchKeywordTrend

YouTube 금융 콘텐츠 검색어와 검색 횟수를 저장합니다. 인기 검색어 표시를 위한 모델입니다.

### CommunityPost, CommunityComment

커뮤니티 게시글과 댓글을 저장합니다. 게시판 종류, 작성자, 제목, 본문, 작성일, 수정일을 관리합니다.

## AI 사용 방식

FinPick은 금융 진단 결과를 기반으로 개인화된 금융 코칭 문장을 제공합니다.

AI가 담당하는 영역은 다음과 같습니다.

- 진단 결과 기반 강점 생성
- 진단 결과 기반 보완점 생성
- 오늘의 금융 메시지 생성
- 추천 상품에 대한 설명 문구 생성
- 금융 유형별 추천 후보 보조

현재 구조는 단순 프롬프트 호출에서 확장되어, 사용자의 취약 영역과 관련 있는 `FinancialGuide` 데이터를 검색한 뒤 AI 프롬프트에 함께 전달합니다. 이 방식은 벡터 DB를 사용하는 완전한 RAG는 아니지만, 추후 금융 가이드 데이터를 늘리고 임베딩 검색을 붙일 수 있는 RAG 확장 구조입니다.

추천 상품은 AI가 직접 임의 선택하지 않습니다. 백엔드가 사용자 진단 결과, 프로필, 상품 금리와 기간 등의 속성을 기준으로 1차 점수화하고, AI는 이미 선정된 상품이 사용자에게 적합한 이유를 쉬운 문장으로 설명합니다.

AI 호출에 필요한 설정이 없으면 일부 기능은 기본 문구 또는 백엔드 규칙 기반 결과로 대체됩니다.

## API 명세

백엔드 URL은 기본적으로 `http://localhost:8000`입니다.

| Method | URL | 설명 |
| ------ | --- | --- |
| GET | `/api/test/` | Django API 연결 테스트 |
| POST | `/api/signup/` | 회원가입 |
| POST | `/api/login/` | 로그인 |
| POST | `/api/logout/` | 로그아웃 |
| GET | `/api/session/` | 현재 세션 및 로그인 사용자 확인 |
| POST | `/api/password-change/` | 로그인 사용자의 비밀번호 변경 |
| POST | `/api/password-reset/` | 아이디와 이름 확인 후 비밀번호 재설정 |
| GET | `/api/dashboard/` | 사용자 대시보드 및 프로필 요약 |
| POST | `/api/diagnosis/` | 금융 진단 생성 |
| GET | `/api/diagnosis/latest/` | 최신 금융 진단 조회 |
| GET | `/api/roadmap/` | 사용자 금융 로드맵 조회 |
| POST | `/api/missions/<mission_id>/toggle/` | 로드맵 미션 완료 여부 토글 |
| GET | `/api/products/` | 초기 추천 상품 목록 조회 |
| GET | `/api/deposit-products/` | 예금/적금 상품 목록 조회 |
| GET | `/api/deposit-products/<product_id>/` | 예금/적금 상품 상세 조회 |
| POST | `/api/deposit-products/<product_id>/join/` | 예금/적금 가입 관심 등록 |
| DELETE | `/api/deposit-products/<product_id>/join/` | 예금/적금 가입 관심 해제 |
| POST | `/api/deposit-products/<product_id>/favorite/` | 예금/적금 관심 상품 토글 |
| GET | `/api/favorite-deposit-products/` | 관심 예금/적금 상품 목록 조회 |
| GET | `/api/stocks/` | 국내 주식 목록 조회 |
| GET | `/api/stocks/<stock_code>/` | 국내 주식 상세 조회 |
| POST | `/api/stocks/<stock_code>/favorite/` | 관심 주식 토글 |
| GET | `/api/ai/test/` | AI 연결 테스트 겸 오늘의 금융 메시지 조회 |
| GET | `/api/ai/product-recommendations/` | 금융 유형별 AI 추천 상품 조회 |
| GET | `/api/ai/diagnosis-summary/` | 최신 진단 기반 AI 요약 조회 |
| GET | `/api/ai/today-message/` | 오늘의 금융 메시지 조회 |
| GET | `/api/ai/recommend-products/` | 점수화 기반 추천 상품과 AI 추천 이유 조회 |
| GET | `/api/youtube/search/` | YouTube 금융 콘텐츠 검색 |
| GET | `/api/youtube/videos/<video_id>/` | YouTube 영상 상세 조회 |
| GET | `/api/trending-keywords/` | 인기 검색어 조회 |
| GET, POST | `/api/community/posts/` | 커뮤니티 게시글 목록 조회 및 작성 |
| GET, POST, DELETE | `/api/community/posts/<post_id>/` | 커뮤니티 게시글 상세, 수정, 삭제 |
| GET, POST | `/api/community/posts/<post_id>/comments/` | 댓글 목록 조회 및 작성 |
| POST, DELETE | `/api/community/comments/<comment_id>/` | 댓글 수정 및 삭제 |
| GET, POST | `/api/profile/` | 사용자 프로필 조회 및 수정 |
| GET | `/api/map-config/` | Kakao Map 설정 조회 |
| GET | `/api/bank-route/` | Kakao Mobility 기반 경로 조회 |
| GET | `/api/spot-prices/` | 로컬 엑셀 파일 기반 금/은 가격 조회 |

## 실행 방법

### Backend

```bash
cd backend
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\activate
```

macOS 또는 Git Bash:

```bash
source venv/Scripts/activate
```

의존성 설치 및 서버 실행:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_finpick
python manage.py runserver
```

금융감독원 예금/적금 상품 데이터를 동기화하려면 `FINLIFE_API_KEY` 설정 후 다음 명령을 실행합니다.

```bash
python manage.py sync_deposit_products
```

Backend 서버 주소:

```text
http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend 서버 주소:

```text
http://localhost:5173
```

프론트엔드는 여러 화면에서 `http://localhost:8000`을 직접 호출하며, Axios 요청에 `withCredentials: true`를 사용해 Django 세션 쿠키를 전달합니다.

## 환경변수 설정

`settings.py`와 관리 명령에서 확인되는 환경변수는 다음과 같습니다. 실제 키 값은 README에 작성하지 말고 `.env`에만 저장해야 합니다.

```env
KAKAO_MAP_APP_KEY=
KAKAO_MOBILITY_REST_KEY=
YOUTUBE_DATA_API_KEY=
KRX_API_KEY=
STOCK_API_KEY=
DATA_GO_KR_API_KEY=
STOCK_API_URL=
GMS_API_KEY=
GMS_OPENAI_BASE_URL=
GMS_BASE_URL=
GMS_OPENAI_MODEL=gpt-4.1-mini
LOGO_DEV_KEY=
FINLIFE_API_KEY=
```

`KRX_API_KEY`는 없을 경우 `STOCK_API_KEY`, `DATA_GO_KR_API_KEY` 순서로 대체 참조됩니다.

`.env`와 `.env.*`는 `.gitignore`에 포함되어 있으므로 민감한 API 키를 커밋하지 않도록 유지해야 합니다.

## 주요 화면

실제 스크린샷 파일이 준비되면 `docs/images/` 경로에 추가할 수 있습니다.

![홈 화면](./docs/images/home.png)

![금융진단 화면](./docs/images/diagnosis.png)

![진단 결과 화면](./docs/images/diagnosis-result.png)

![로드맵 화면](./docs/images/roadmap.png)

![추천상품 화면](./docs/images/products.png)

![주식 화면](./docs/images/stocks.png)

![내 정보 화면](./docs/images/profile.png)

![커뮤니티 화면](./docs/images/community.png)

## 트러블슈팅

### 프론트엔드에서 로그인 세션이 유지되지 않는 경우

- Axios 요청에 `withCredentials: true`가 포함되어 있는지 확인합니다.
- Django `CORS_ALLOWED_ORIGINS`에 프론트엔드 개발 서버 주소가 포함되어 있는지 확인합니다.
- 현재 설정에는 `http://localhost:5173`, `http://localhost:5174`가 허용되어 있습니다.
- 브라우저 개발자 도구에서 세션 쿠키가 전달되는지 확인합니다.

### 공공데이터 API가 401 Unauthorized를 반환하는 경우

- `.env`의 API 키 이름이 `settings.py`에서 참조하는 이름과 일치하는지 확인합니다.
- 주식 API는 `KRX_API_KEY`, `STOCK_API_KEY`, `DATA_GO_KR_API_KEY` 중 하나를 참조합니다.
- 공공데이터포털의 인코딩 키와 디코딩 키 사용 방식이 API 요청 방식과 맞는지 확인합니다.

### 예금/적금 상품 데이터가 비어 있는 경우

- `FINLIFE_API_KEY`를 설정했는지 확인합니다.
- `python manage.py sync_deposit_products` 명령을 실행해 금융상품 데이터를 동기화합니다.
- 네트워크 또는 금융감독원 API 응답 오류가 없는지 터미널 로그를 확인합니다.

### Vue Router 이동 후 화면 또는 내비게이션이 어색한 경우

- `frontend/src/App.vue`의 공통 레이아웃과 `RouterView` 구조를 확인합니다.
- 로그인 필요 화면은 라우터 메타의 `requiresAuth`와 세션 확인 로직의 영향을 받습니다.

### 주식 데이터가 중복 표시되는 경우

- 백엔드에는 종목 코드와 기준일을 바탕으로 최신 데이터만 남기는 `deduplicate_latest_stocks` 흐름이 포함되어 있습니다.
- 외부 API 응답에 동일 종목의 여러 기준일 데이터가 섞여 있는지 확인합니다.

### AI 응답이 생성되지 않는 경우

- `GMS_API_KEY`와 `GMS_OPENAI_BASE_URL`이 설정되어 있는지 확인합니다.
- OpenAI 호환 게이트웨이에서 `GMS_OPENAI_MODEL` 값이 사용 가능한 모델인지 확인합니다.
- 설정이 없으면 일부 AI 기능은 기본 문구 또는 규칙 기반 결과로 대체됩니다.

### 의존성 설치 오류가 발생하는 경우

- 백엔드는 `backend/requirements.txt`를 기준으로 설치합니다.
- 프론트엔드는 `frontend/package.json` 기준으로 `npm install`을 실행합니다.
- 현재 프론트엔드 `package.json`은 Node `^22.18.0 || >=24.12.0` 엔진 범위를 명시합니다.

## 팀원 및 역할

| 이름 | 역할 |
| ---- | ---- |
| 박지훈 | Django/Vue 기능 구현|
| 문지수 | 금융진단·로드맵·맞춤형 추천, 외부 API 연동 |


## 향후 개선 방향

- 금융 가이드 데이터 확장
- 벡터 DB 기반 RAG 검색 고도화
- 카드 상품 데이터 연동 및 추천 기능 추가
- 관심 상품 기능 고도화
- 커뮤니티 북마크, 좋아요, 신고 기능 추가
- 사용자 자산 데이터 기반 추천 정확도 개선
- 배포 환경에서 환경변수와 보안 설정 분리
- 주식 및 예금/적금 외부 API 장애 시 캐싱 전략 강화
- README 스크린샷 이미지 추가


## 프로젝트 후기 및 느낀 점

- 이번 프로젝트를 진행하면서 가장 힘들었던 부분은 금융 진단, 성장 로드맵, 추천 상품 기능을 각각 따로 구현하는 것이 아니라 하나의 흐름으로 연결하는 과정이었습니다. 처음에는 금융 진단은 설문 결과를 저장하는 기능, 로드맵은 미션을 보여주는 기능, 추천 상품은 상품 목록을 보여주는 기능이라고 단순하게 생각했습니다. 하지만 실제로 구현해보니 세 기능은 모두 사용자의 최신 금융 진단 결과를 기준으로 움직여야 했고, 진단 결과가 바뀌면 로드맵과 추천 상품도 함께 달라져야 했습니다. 이 흐름을 맞추기 위해 데이터 모델, API 응답 구조, 프론트 화면 상태를 계속 확인하며 수정하는 과정이 특히 어려웠습니다.

- 추천 상품 기능을 구현하는 과정도 많은 고민이 필요했습니다. 단순히 금리가 높은 상품을 추천하면 구현은 쉬웠지만, 사회초년생을 위한 맞춤형 금융 서비스라는 프로젝트 목적과는 맞지 않았습니다. 그래서 사용자의 투자 경험, 안정성 점수, 금융 준비도, 상품 금리와 기간 등을 함께 고려해 점수화하는 방식으로 구현했습니다. 이 과정에서 추천 로직은 단순히 데이터를 정렬하는 것이 아니라, 서비스가 어떤 기준으로 사용자를 도울 것인지 정하는 일이라는 것을 배웠습니다.

- 또한 AI 기능을 붙이면서도 어려움이 있었습니다. AI가 모든 판단을 대신하게 하면 결과를 설명하기 어렵고 신뢰도도 떨어질 수 있다고 생각했습니다. 그래서 핵심 판단은 백엔드 규칙 기반으로 처리하고, AI는 강점과 보완점, 추천 이유를 자연스럽게 설명하는 보조 역할로 제한했습니다. 이 과정을 통해 AI는 무조건 많이 사용하는 것이 중요한 것이 아니라, 서비스 흐름 안에서 적절한 역할을 정하는 것이 중요하다는 점을 배웠습니다.

- 이번 프로젝트를 통해 Django 백엔드와 Vue 프론트엔드를 연결하는 과정, 세션 인증, CORS 설정, 외부 API 연동, 예외 처리 등 실제 서비스에 가까운 흐름을 경험할 수 있어서 좋았습니다. 앞으로는 처음부터 데이터 흐름과 기능 간 연결 관계를 더 명확하게 설계하고, 추천 기준이나 예외 상황도 문서화하면서 개발하고 싶습니다. 또한 향후에는 금융 가이드 데이터를 더 확장하고, 벡터 DB 기반 RAG나 사용자 자산 데이터 연동을 통해 더 정확하고 신뢰할 수 있는 추천 서비스로 발전시킬 수 있으면 좋겠습니다.