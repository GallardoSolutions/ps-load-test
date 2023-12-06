import os
import yaml


class PromoConfig:

    def __init__(self, supplier_code: str, environment: str):
        self.data = self.get_config_data()
        self.supplier_code = supplier_code
        self.environment_url = 'prod_url' if environment == 'production' else 'stage_url'

    @staticmethod
    def get_config_data():
        config_file = os.path.join("config.yaml")
        with open(config_file, 'r') as config:
            return yaml.safe_load(config)

    def get_url(self, service: str, service_version: str):
        return self.data[self.supplier_code]["services"][service][service_version][self.environment_url]
