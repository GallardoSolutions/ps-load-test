import os
from datetime import datetime, timedelta

from jinja2 import Environment, FileSystemLoader
import yaml
from locust import HttpUser, task, between

DEBUG = int(os.getenv('DEBUG', 0))  # be careful only 0/1 are should be valid values
ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging').lower()
ENVIRONMENT_URL = 'prod_url' if ENVIRONMENT == 'production' else 'stage_url'
SUPPLIER_CODE = os.getenv('SUPPLIER_CODE', 'HIT')
T_SHIRT_PRODUCT_CODE = os.getenv('T_SHIRT_PRODUCT_CODE', '3001C')
HARD_GOODS_PRODUCT_CODE = os.getenv('HARD_GOODS_PRODUCT_CODE', '1001')

now = datetime.now()
now = now.replace(hour=0, minute=0, second=0, microsecond=0)
last_week = now - timedelta(days=7)


class PromoConfig:

    def __init__(self):
        self.data = self.get_config_data()

    @staticmethod
    def get_config_data():
        config_file = os.path.join("config.yaml")
        with open(config_file, 'r') as config:
            return yaml.safe_load(config)

    def get_url(self, service: str, service_version: str):
        return self.data[SUPPLIER_CODE]["services"][service][service_version][ENVIRONMENT_URL]


class SoapUserMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.config = PromoConfig()
        self.username = os.getenv('PROMO_USERNAME')
        self.password = os.getenv('PROMO_PASSWORD')

    def post(self, service: str, service_version: str, template_path: str, soap_action: str, context: dict):
        template = self.env.get_template(template_path)
        context |= {'username': self.username, 'password': self.password}
        soap_request_body = template.render(**context)

        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': soap_action
        }
        url = self.get_service_url(service, service_version)
        ret = self._post(url, soap_action, soap_request_body, headers)
        return ret

    def _post(self, url, soap_action, soap_request_body, headers):
        if DEBUG:
            print(f'url: {url}')
            print(f'soap_action: {soap_action}')
            print(f'soap_request_body: {soap_request_body}')
        ret = self.client.post(url, name=soap_action, data=soap_request_body, headers=headers)
        if DEBUG:
            print(f'status_code: {ret.status_code}')
            print(f'response: {ret.text}')
        return ret

    def get_service_url(self, service: str, service_version: str):
        return self.config.get_url(service, service_version)


class PromoStandardsUser(SoapUserMixin, HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def get_product_sellable(self):
        soap_action = 'getProductSellable'
        context = {
            'productId': None, 'isSellable': True,
            'localizationCountry': 'US', 'localizationLanguage': 'en', 'wsVersion': '2.0.0',
        }

        self.post('Product', '2.0.0',
                  'product-data/version-2-0-0/get-sellables.xml', soap_action, context)

    @task(10)
    def get_product(self):
        soap_action = 'getProduct'
        context = {
            'productId': T_SHIRT_PRODUCT_CODE,
            'localizationCountry': 'US', 'localizationLanguage': 'en', 'wsVersion': '2.0.0',
        }

        self.post('Product', '2.0.0',
                  'product-data/version-2-0-0/get-product.xml', soap_action, context)

    @task(1)
    def get_product_date_modified(self):
        soap_action = 'getProductDateModified'
        context = {
            'changeTimeStamp': last_week.isoformat(), 'wsVersion': '2.0.0',
        }
        self.post('Product', '2.0.0',
                  'product-data/version-2-0-0/get-product-date-modified.xml', soap_action, context)

    @task(1)
    def get_product_close_out(self):
        soap_action = 'getProductCloseOut'
        context = {
            'wsVersion': '2.0.0',
        }
        self.post('Product', '2.0.0',
                  'product-data/version-2-0-0/get-product-closeout.xml', soap_action, context)
