import logging
from typing import Generator

from spaceone.core.error import *
from spaceone.core.manager import BaseManager
from cloudforet.plugin.lib.model.resource_info_model import ResourceInfo, State
from cloudforet.plugin.lib.model.plugin_info_model import ResourceType
from cloudforet.plugin.model.collector import CollectorPluginInfo

_LOGGER = logging.getLogger(__name__)


class CollectorManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = None
        self.cloud_service_type = None
        self.region_name = None
        self.provider = None

    def init_response(self, options: dict) -> dict:
        response = CollectorPluginInfo()
        return response.dict()

    def verify_client(self, options: dict, secret_data: dict, schema: str) -> None:
        raise NotImplementedError('Method not implemented!')

    def collect(self, options: dict, secret_data: dict, schema: str) -> Generator[dict, None, None]:
        raise NotImplementedError('Method not implemented!')

    @staticmethod
    def validate_response(resource_data):
        response = ResourceInfo(**resource_data)
        return response.dict()

    def make_response(self, resource_data: dict, match_rules: dict,
                      resource_type: str = 'inventory.CloudService') -> dict:
        return self.validate_response({
            'state': State.success,
            'resource_type': resource_type,
            'match_rules': match_rules,
            'resource': resource_data
        })

    def error_response(self, error: Exception, resource_type: str = 'inventory.CloudService') -> dict:
        if not isinstance(error, ERROR_BASE):
            error = ERROR_UNKNOWN(message=error)

        _LOGGER.error(f'[error_response] ({self.region_name}) {error.error_code}: {error.message}', exc_info=True)
        return self.validate_response({
            'state': State.failre,
            'message': error.message,
            'resource_type': ResourceType.error,
            'resource': {
                'provider': self.provider,
                'cloud_service_group': self.cloud_service_group,
                'cloud_service_type': self.cloud_service_type,
                'resource_type': resource_type
            }
        })

    @staticmethod
    def validate_response(resource_data):
        response = ResourceInfo(**resource_data)
        return response.dict()
