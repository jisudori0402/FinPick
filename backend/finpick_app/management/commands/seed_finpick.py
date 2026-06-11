from django.core.management.base import BaseCommand
from finpick_app.models import RoadmapStep, ProductRecommendation


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

        self.stdout.write(self.style.SUCCESS('FinPick seed data ready.'))
