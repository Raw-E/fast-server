"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for save_api_operation.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports
# Add any standard library imports to this section

# Third-Party Imports
# Add any third-party imports to this section
from fastapi import Request
from pydantic import BaseModel

# Local Development Imports
from fast_server.v1 import (
    APIOperation,
    HTTPMethod,
)
from foundation.v1 import CustomLogger

# Current Project Imports
from ..data_model_handlers.idea_data_model_handler import IdeaDataModelHandler
from ..data_models.idea_data_model import IdeaDataModel
from ...utilities.get_user_id_with_authentication_header import get_user_id_with_authentication_header

# Type Variables
# Define type variables in this section

# Type Aliases
# Define type aliases in this section

# Constants
# Define constants in this section

# Configuration
# Setup configuration in this section
logger = CustomLogger(log_level="INFO")


# Data Schemas
class RequestSchema(BaseModel):
    class Body(BaseModel):
        idea: IdeaDataModel


class ResponseSchema(BaseModel):
    success: bool


# Main Classes
class SaveIdeaApiOperation(APIOperation):
    ENDPOINT_PATH: str = "/save-idea"
    METHOD: HTTPMethod = HTTPMethod.POST
    REQUEST_SCHEMA = RequestSchema
    RESPONSE_SCHEMA = ResponseSchema
    DETAILED_REQUEST_LOGGING_ENABLED: bool = True

    async def execute(
        self,
        request: Request,
        body: RequestSchema.Body,
    ) -> ResponseSchema:
        user_id: str = get_user_id_with_authentication_header(request.headers.get("authorization"))

        document: dict = body.idea.to_mongodb_dictionary()
        document["userId"] = user_id

        await IdeaDataModelHandler.insert(document)

        return ResponseSchema(success=True)
