from django.core.management.base import BaseCommand
from finpick_app.models import FinancialGuide, RoadmapStep, ProductRecommendation


class Command(BaseCommand):
    help = 'Seed initial FinPick roadmap and product data'

    def handle(self, *args, **options):
        RoadmapStep.objects.all().delete()
        ProductRecommendation.objects.all().delete()

        RoadmapStep.objects.bulk_create([
            RoadmapStep(step_number=1, title='비상금 300만원 만들기', description='예상치 못한 지출에 대비하기 위한 기초 자금 마련'),
            RoadmapStep(step_number=2, title='청년도약계좌 가입 검토', description='목돈 마련을 위한 정부 지원 금융상품 확인'),
            RoadmapStep(step_number=3, title='생활비 카드 정리', description='소비 패턴에 맞는 카드로 고정비 절약'),
            RoadmapStep(step_number=4, title='ISA 계좌 개설', description='투자를 시작하기 전 절세 계좌 기반 마련'),
        ])

        ProductRecommendation.objects.bulk_create([
            ProductRecommendation(name='고금리 입출금 통장', product_type='비상금 관리용', reason='비상금을 안전하게 보관하면서 이자도 받을 수 있어요.', category='savings'),
            ProductRecommendation(name='청년도약계좌', product_type='목돈 마련용', reason='사회초년생의 장기 저축에 적합해요.', category='savings'),
            ProductRecommendation(name='생활비 할인 체크카드', product_type='소비 절약용', reason='편의점, 교통, 카페 소비가 많은 사용자에게 적합해요.', category='card'),
        ])

        guide_rows = [
            ('비상금', '비상금 3개월 원칙', '비상금은 최소 3개월치 생활비를 확보하는 것이 좋다.', '비상금,생활비,안정성,현금흐름'),
            ('소비', '고정비 먼저 점검하기', '소비 점수가 낮은 사용자는 고정비와 구독 서비스를 먼저 점검하는 것이 좋다.', '소비,고정비,구독,지출'),
            ('저축', '월급일 다음 날 자동이체', '저축 습관을 만들기 위해 월급일 다음 날 자동이체를 설정하는 것이 좋다.', '저축,자동이체,월급,습관'),
            ('투자', '기초 상품부터 이해하기', '투자 경험이 부족한 사용자는 고위험 상품보다 예적금, CMA, ISA 같은 기초 상품부터 이해하는 것이 좋다.', '투자,예적금,CMA,ISA,위험'),
            ('사회초년생', '현금흐름 우선', '사회초년생은 수익률보다 현금흐름 관리와 비상금 확보를 우선해야 한다.', '사회초년생,현금흐름,비상금,수익률'),
            ('안정성', '단기 목표 자금 관리', '단기 목표 자금은 원금 손실 가능성이 낮은 상품을 우선 고려하는 것이 좋다.', '안정성,단기목표,원금손실,예금,적금'),
        ]
        for category, title, content, keywords in guide_rows:
            FinancialGuide.objects.update_or_create(
                category=category,
                title=title,
                defaults={'content': content, 'keywords': keywords},
            )

        self.stdout.write(self.style.SUCCESS('FinPick seed data ready.'))
