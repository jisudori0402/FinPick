# FinPick ERD

이 문서는 `backend/finpick_app/models.py` 기준으로 정리한 FinPick 데이터 모델 ERD입니다.

## 전체 ERD

```mermaid
erDiagram
    AUTH_USER {
        int id PK
        string username
        string email
        string first_name
        string password
        boolean is_active
        boolean is_staff
        datetime date_joined
    }

    USER_PROFILE {
        int id PK
        int user_id FK
        date birth_date
        int age
        string job
        int monthly_income
        int monthly_expense
        string residence_type
        string saving_status
        string invest_experience
        text intro
        file profile_image
        datetime created_at
        datetime password_changed_at
    }

    DIAGNOSIS_RESULT {
        int id PK
        int user_id FK
        string name
        string income
        string expense
        string saving
        string invest
        string income_level
        string spending_style
        string financial_goal
        string investment_style
        string asset_level
        string loan_type
        string financial_type
        int readiness_score
        text strengths
        text improvements
        text finpick_comment
        json profile_scores
        string level
        text summary
        datetime created_at
    }

    ROADMAP_STEP {
        int id PK
        int step_number
        string title
        text description
    }

    ROADMAP_TEMPLATE {
        int id PK
        string type_code
        int level
        string title
        text description
        int order
    }

    ROADMAP_MISSION {
        int id PK
        int roadmap_template_id FK
        string mission_title
        text mission_description
        string category
        int order
    }

    USER_MISSION {
        int id PK
        int user_id FK
        int mission_id FK
        boolean is_completed
        datetime completed_at
    }

    PRODUCT_RECOMMENDATION {
        int id PK
        string name
        string product_type
        text reason
        string category
    }

    DAILY_FINANCIAL_TIP {
        int id PK
        date tip_date UK
        text message
        datetime created_at
    }

    AI_PRODUCT_RECOMMENDATION {
        int id PK
        date recommendation_date
        string financial_type
        json deposit_product_ids
        json stock_codes
        json stock_items
        datetime created_at
    }

    FINANCIAL_GUIDE {
        int id PK
        string category
        string title
        text content
        string keywords
        datetime created_at
        datetime updated_at
    }

    SEARCH_KEYWORD_TREND {
        int id PK
        string keyword UK
        int search_count
        datetime last_searched_at
        datetime created_at
    }

    DEPOSIT_PRODUCT {
        int id PK
        string product_type
        string disclosure_month
        string financial_company_code
        string financial_company_name
        string product_code
        string product_name
        text join_way
        text maturity_interest
        text special_condition
        string join_deny
        text join_member
        text etc_note
        bigint max_limit
        json raw_data
        datetime updated_at
        datetime created_at
    }

    DEPOSIT_OPTION {
        int id PK
        int product_id FK
        string interest_rate_type
        string interest_rate_type_name
        int saving_term
        decimal interest_rate
        decimal max_interest_rate
        string reserve_type
        string reserve_type_name
        json raw_data
        datetime updated_at
        datetime created_at
    }

    USER_DEPOSIT_SUBSCRIPTION {
        int id PK
        int user_id FK
        int product_id FK
        datetime created_at
    }

    USER_FAVORITE_DEPOSIT_PRODUCT {
        int id PK
        int user_id FK
        int product_id FK
        datetime created_at
    }

    USER_FAVORITE_STOCK {
        int id PK
        int user_id FK
        string code
        string isin_code
        string name
        string market
        string base_date
        bigint current_price
        bigint change
        float change_rate
        bigint volume
        bigint market_cap
        datetime created_at
        datetime updated_at
    }

    COMMUNITY_POST {
        int id PK
        int author_id FK
        string board
        string title
        text content
        datetime created_at
        datetime updated_at
    }

    COMMUNITY_COMMENT {
        int id PK
        int post_id FK
        int author_id FK
        text content
        datetime created_at
        datetime updated_at
    }

    AUTH_USER ||--|| USER_PROFILE : has
    AUTH_USER ||--o{ DIAGNOSIS_RESULT : writes
    AUTH_USER ||--o{ USER_MISSION : owns
    AUTH_USER ||--o{ USER_DEPOSIT_SUBSCRIPTION : subscribes
    AUTH_USER ||--o{ USER_FAVORITE_DEPOSIT_PRODUCT : favorites
    AUTH_USER ||--o{ USER_FAVORITE_STOCK : favorites
    AUTH_USER ||--o{ COMMUNITY_POST : writes
    AUTH_USER ||--o{ COMMUNITY_COMMENT : writes

    ROADMAP_TEMPLATE ||--o{ ROADMAP_MISSION : contains
    ROADMAP_MISSION ||--o{ USER_MISSION : assigned_as

    DEPOSIT_PRODUCT ||--o{ DEPOSIT_OPTION : has
    DEPOSIT_PRODUCT ||--o{ USER_DEPOSIT_SUBSCRIPTION : selected_by
    DEPOSIT_PRODUCT ||--o{ USER_FAVORITE_DEPOSIT_PRODUCT : favorited_by

    COMMUNITY_POST ||--o{ COMMUNITY_COMMENT : has
```

## 주요 관계 요약

| 관계 | 설명 |
| --- | --- |
| `AUTH_USER` 1:1 `USER_PROFILE` | 사용자 계정별 프로필 정보 |
| `AUTH_USER` 1:N `DIAGNOSIS_RESULT` | 사용자별 금융 진단 이력 |
| `ROADMAP_TEMPLATE` 1:N `ROADMAP_MISSION` | 금융 유형/단계별 미션 템플릿 |
| `AUTH_USER` N:M `ROADMAP_MISSION` | `USER_MISSION`을 통한 사용자별 미션 완료 상태 |
| `DEPOSIT_PRODUCT` 1:N `DEPOSIT_OPTION` | 예금/적금 상품별 금리 옵션 |
| `AUTH_USER` N:M `DEPOSIT_PRODUCT` | 가입 관심 모델과 즐겨찾기 모델로 분리 관리 |
| `AUTH_USER` 1:N `USER_FAVORITE_STOCK` | 사용자별 관심 주식 저장 |
| `AUTH_USER` 1:N `COMMUNITY_POST` | 사용자별 커뮤니티 게시글 |
| `COMMUNITY_POST` 1:N `COMMUNITY_COMMENT` | 게시글별 댓글 |
| `AUTH_USER` 1:N `COMMUNITY_COMMENT` | 사용자별 댓글 |

## 제약 조건

| 모델 | 제약 |
| --- | --- |
| `RoadmapTemplate` | `type_code`, `level` 조합 unique |
| `RoadmapMission` | `roadmap_template`, `mission_title` 조합 unique |
| `UserMission` | `user`, `mission` 조합 unique |
| `DailyFinancialTip` | `tip_date` unique |
| `AiProductRecommendation` | `recommendation_date`, `financial_type` 조합 unique |
| `FinancialGuide` | `category`, `title` 조합 unique |
| `SearchKeywordTrend` | `keyword` unique |
| `DepositProduct` | `product_type`, `financial_company_code`, `product_code` 조합 unique |
| `DepositOption` | `product`, `saving_term`, `interest_rate_type`, `reserve_type` 조합 unique |
| `UserDepositSubscription` | `user`, `product` 조합 unique |
| `UserFavoriteDepositProduct` | `user`, `product` 조합 unique |
| `UserFavoriteStock` | `user`, `code` 조합 unique |

## 독립 테이블

다음 모델은 현재 코드상 명시적인 ForeignKey 없이 독립적으로 사용됩니다.

- `RoadmapStep`
- `ProductRecommendation`
- `DailyFinancialTip`
- `AiProductRecommendation`
- `FinancialGuide`
- `SearchKeywordTrend`

