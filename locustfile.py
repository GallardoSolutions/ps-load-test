import os
from datetime import datetime, timedelta
import logging

from jinja2 import Environment, FileSystemLoader
from locust import HttpUser, task, between

from promo_config import PromoConfig
from template_helper import TemplateHelper

ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging').lower()
SUPPLIER_CODE = os.getenv('SUPPLIER_CODE', 'HIT')
T_SHIRT_PRODUCT_CODE = os.getenv('T_SHIRT_PRODUCT_CODE', '3001C')
HARD_GOODS_PRODUCT_CODE = os.getenv('HARD_GOODS_PRODUCT_CODE', '1001')

now = datetime.now()
now = now.replace(hour=0, minute=0, second=0, microsecond=0)
last_week = now - timedelta(days=7)


def log_starting_info():
    logging.info(f'ENVIRONMENT: {ENVIRONMENT}')
    logging.info(f'SUPPLIER_CODE: {SUPPLIER_CODE}')
    logging.info(f'T_SHIRT_PRODUCT_CODE: {T_SHIRT_PRODUCT_CODE}')
    logging.info(f'HARD_GOODS_PRODUCT_CODE: {HARD_GOODS_PRODUCT_CODE}')


class SoapUserMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.config = PromoConfig(SUPPLIER_CODE, ENVIRONMENT)
        self.username = os.getenv('PROMO_USERNAME')
        self.password = os.getenv('PROMO_PASSWORD')

    def post(self, service: str, service_version: str, soap_action: str, context: dict):
        template_path = TemplateHelper.get_template_path(service, service_version, soap_action)
        template = self.env.get_template(template_path)
        context |= {'username': self.username, 'password': self.password, 'wsVersion': service_version}
        soap_request_body = template.render(**context)

        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': soap_action
        }
        url = self.get_service_url(service, service_version)
        ret = self._post(url, soap_action, soap_request_body, headers)
        return ret

    def _post(self, url, soap_action, soap_request_body, headers):
        logging.debug(f'url: {url}')
        logging.debug(f'soap_action: {soap_action}')
        logging.debug(f'soap_request_body: {soap_request_body}')
        ret = self.client.post(url, name=soap_action, data=soap_request_body, headers=headers)
        logging.debug(f'status_code: {ret.status_code}')
        logging.debug(f'response: {ret.text}')
        logging.debug('=' * 100)
        return ret

    def get_service_url(self, service: str, service_version: str):
        return self.config.get_url(service, service_version)


class PromoStandardsUser(SoapUserMixin, HttpUser):
    wait_time = between(1, 5)


    @task(1)
    def get_product_sellable(self):
        soap_action = 'getProductSellable'
        context = {
            'isSellable': True,
            'localizationCountry': 'US', 'localizationLanguage': 'en',
        }

        self.post('Product', '2.0.0', soap_action, context)

    @task(10)
    def get_product(self):
        soap_action = 'getProduct'
        context = {
            'productId': T_SHIRT_PRODUCT_CODE,
            'localizationCountry': 'US', 'localizationLanguage': 'en',
        }

        self.post('Product', '2.0.0', soap_action, context)

    @task(1)
    def get_product_date_modified(self):
        soap_action = 'getProductDateModified'
        context = {
            'changeTimeStamp': last_week.isoformat(),
        }
        self.post('Product', '2.0.0', soap_action, context)

    @task(1)
    def get_product_close_out(self):
        soap_action = 'getProductCloseOut'
        context = {}
        self.post('Product', '2.0.0', soap_action, context)

    @task(1)
    def get_media_content(self):
        soap_action = 'getMediaContent'
        context = {
            'mediaType': 'Image',
            'productId': T_SHIRT_PRODUCT_CODE,
        }
        self.post('MED', '1.1.0', soap_action, context)

    @task(1)
    def get_media_date_modified(self):
        soap_action = 'getMediaDateModified'
        context = {
            'productId': T_SHIRT_PRODUCT_CODE,
            'cultureName': 'us-en',
            'changeTimeStamp': last_week.isoformat(),
        }
        self.post('MED', '1.1.0', soap_action, context)


if __name__ == '__main__':
    log_starting_info()
