# Standard library imports
from abc import abstractmethod
from typing import Optional, Type

# Third-party imports
from fastapi import Depends
from pydantic import BaseModel

# Local application imports
from foundation.v1 import ABCSingletonMetaclass, CustomLogger, Operation

from ..api_operation_dependencies.log_request_data import log_request_data
from ..http_methods import HTTPMethod

# Configuration
logger = CustomLogger(log_level="INFO")


class APIOperation(Operation, metaclass=ABCSingletonMetaclass):
    ENDPOINT_PATH: str
    METHOD: HTTPMethod = HTTPMethod.GET
    REQUEST_SCHEMA: Optional[Type[BaseModel]] = None
    RESPONSE_SCHEMA: Type[BaseModel]
    DETAILED_REQUEST_LOGGING_ENABLED: bool = False

    def __init__(self):
        self.dependencies = []
        self._add_standard_dependencies()

    @abstractmethod
    async def execute(self, *args, **kwargs) -> BaseModel:
        pass

    def add_dependency(self, dependency) -> None:
        self.dependencies.append(Depends(dependency))

    def _add_standard_dependencies(self) -> None:
        if self.DETAILED_REQUEST_LOGGING_ENABLED:
            self.add_dependency(log_request_data)
