"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for get_health.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports
# Add any standard library imports to this section

# Third-Party Imports
# Add any third-party imports to this section
from typing import Type

from pydantic import BaseModel

# Local Development Imports
from fast_server.v1 import (
    APIOperation,
    HTTPMethod,
)
from foundation.v1 import CustomLogger

# Add any local development imports to this section

# Current Project Imports
# Add any current project imports to this section

# Type Variables
# Define type variables in this section

# Type Aliases
# Define type aliases in this section

# Constants
# Define constants in this section

# Configuration
# Setup configuration in this section
logger = CustomLogger(log_level="INFO")


class HealthCheckResponseSchema(BaseModel):
    is_healthy: bool


class GetHealth(APIOperation):
    RESPONSE_SCHEMA: Type[HealthCheckResponseSchema] = HealthCheckResponseSchema

    ENDPOINT_PATH: str = "/api/health"
    METHOD: HTTPMethod = HTTPMethod.GET

    async def execute(self) -> HealthCheckResponseSchema:
        try:
            logger.info("Health check passed")
            return HealthCheckResponseSchema(is_healthy=True)
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return HealthCheckResponseSchema(is_healthy=False)
