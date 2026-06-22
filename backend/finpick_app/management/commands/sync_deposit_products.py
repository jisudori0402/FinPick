import os
from decimal import Decimal, InvalidOperation

import requests
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv

from finpick_app.models import DepositOption, DepositProduct


FINLIFE_BASE_URL = 'https://finlife.fss.or.kr/finlifeapi'
PRODUCT_APIS = {
    'deposit': 'depositProductsSearch.json',
    'saving': 'savingProductsSearch.json',
}


class Command(BaseCommand):
    help = '금융상품통합비교공시 API에서 예적금 상품과 옵션 데이터를 가져와 저장합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--kind',
            choices=['all', 'deposit', 'saving'],
            default='all',
            help='가져올 상품 종류입니다. 기본값은 all입니다.',
        )
        parser.add_argument(
            '--top-fin-grp-no',
            default='020000',
            help='권역 코드입니다. 기본값 020000은 은행입니다.',
        )

    def handle(self, *args, **options):
        load_dotenv()
        api_key = os.getenv('FINLIFE_API_KEY')
        if not api_key:
            raise CommandError('backend/.env에 FINLIFE_API_KEY 값을 설정해 주세요.')

        kinds = ['deposit', 'saving'] if options['kind'] == 'all' else [options['kind']]
        totals = {'products_created': 0, 'products_updated': 0, 'options_created': 0, 'options_updated': 0}

        for kind in kinds:
            result = self.sync_kind(kind, api_key, options['top_fin_grp_no'])
            for key, value in result.items():
                totals[key] += value

        self.stdout.write(self.style.SUCCESS(
            '예적금 데이터 저장 완료: '
            f"상품 신규 {totals['products_created']}개, "
            f"상품 갱신 {totals['products_updated']}개, "
            f"옵션 신규 {totals['options_created']}개, "
            f"옵션 갱신 {totals['options_updated']}개"
        ))

    def sync_kind(self, kind, api_key, top_fin_grp_no):
        endpoint = PRODUCT_APIS[kind]
        page_no = 1
        max_page_no = 1
        counts = {'products_created': 0, 'products_updated': 0, 'options_created': 0, 'options_updated': 0}

        while page_no <= max_page_no:
            data = self.fetch_page(endpoint, api_key, top_fin_grp_no, page_no)
            result = data.get('result', {})
            max_page_no = int(result.get('max_page_no') or 1)

            product_map = {}
            for item in result.get('baseList', []):
                product, created = self.save_product(kind, item)
                product_map[(product.financial_company_code, product.product_code)] = product
                counts['products_created' if created else 'products_updated'] += 1

            for item in result.get('optionList', []):
                product = product_map.get((item.get('fin_co_no', ''), item.get('fin_prdt_cd', '')))
                if product is None:
                    product = DepositProduct.objects.filter(
                        product_type=kind,
                        financial_company_code=item.get('fin_co_no', ''),
                        product_code=item.get('fin_prdt_cd', ''),
                    ).first()
                if product is None:
                    continue

                _, created = self.save_option(product, item)
                counts['options_created' if created else 'options_updated'] += 1

            page_no += 1

        return counts

    def fetch_page(self, endpoint, api_key, top_fin_grp_no, page_no):
        response = requests.get(
            f'{FINLIFE_BASE_URL}/{endpoint}',
            params={
                'auth': api_key,
                'topFinGrpNo': top_fin_grp_no,
                'pageNo': page_no,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        result = data.get('result', {})
        if result.get('err_cd') not in (None, '000'):
            raise CommandError(f"API 오류: {result.get('err_cd')} {result.get('err_msg')}")
        return data

    def save_product(self, kind, item):
        product, created = DepositProduct.objects.update_or_create(
            product_type=kind,
            financial_company_code=item.get('fin_co_no', ''),
            product_code=item.get('fin_prdt_cd', ''),
            defaults={
                'disclosure_month': item.get('dcls_month', ''),
                'financial_company_name': item.get('kor_co_nm', ''),
                'product_name': item.get('fin_prdt_nm', ''),
                'join_way': item.get('join_way', ''),
                'maturity_interest': item.get('mtrt_int', ''),
                'special_condition': item.get('spcl_cnd', ''),
                'join_deny': item.get('join_deny', ''),
                'join_member': item.get('join_member', ''),
                'etc_note': item.get('etc_note', ''),
                'max_limit': self.to_int(item.get('max_limit')),
                'raw_data': item,
            },
        )
        return product, created

    def save_option(self, product, item):
        option, created = DepositOption.objects.update_or_create(
            product=product,
            saving_term=self.to_int(item.get('save_trm')),
            interest_rate_type=item.get('intr_rate_type', ''),
            reserve_type=item.get('rsrv_type', ''),
            defaults={
                'interest_rate_type_name': item.get('intr_rate_type_nm', ''),
                'interest_rate': self.to_decimal(item.get('intr_rate')),
                'max_interest_rate': self.to_decimal(item.get('intr_rate2')),
                'reserve_type_name': item.get('rsrv_type_nm', ''),
                'raw_data': item,
            },
        )
        return option, created

    def to_decimal(self, value):
        if value in (None, ''):
            return None
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return None

    def to_int(self, value):
        if value in (None, ''):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
