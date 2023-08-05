"""
    Personalize abstract manager module
"""
from sdc_engine_helpers.manager import Manager as BaseManager

class Manager(BaseManager):
    """
        Abstract manager class to be inherited by various Personalize managers
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_slug = kwargs.pop('service_slug', 'recommend')
        self.service = self.query_helper.get_service(
            slug=self.service_slug,
            for_update=self.service_for_update
        )
        self.engine_slug = kwargs.pop('engine_slug', 'personalize')
