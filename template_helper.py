from utils import camel_to_kebab


class TemplateHelper:
    """
    Helps to generate path to template file
    """
    trans = {
        'Product': 'product-data',
        'MED': 'media-content',
        'PPC': 'product-pricing-and-configuration',
        'INV': 'inventory',
        'PO': 'purchase-order',
        'ODRSTAT': 'order-status',
        'OSN': 'order-shipment-notification',
        'INVC': 'invoice',

    }

    @classmethod
    def get_template_path(cls, service: str, version: str, soap_action: str) -> str:
        service_path = cls.trans[service]
        version_path = f'version-{version}'.replace('.', '-')
        action_path = 'get-fob-points' if soap_action == 'getFOBPoints' else camel_to_kebab(soap_action)
        return f'{service_path}/{version_path}/{action_path}.xml'
