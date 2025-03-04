# THIS CODE HAS BEEN ORGANIZED

"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for get_user_id_with_authentication_header.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports
from typing import Optional

# Third-Party Imports
from fastapi import HTTPException

# Local Development Imports
from foundation.v1 import CustomLogger

# Constants
AUTHORIZATION_TOKEN_TO_USER_ID_MAPPING = {
    "test-user-authentication-token": "id-of-test-user",
    "woke-bloke-authentication-token": "id-of-woke-bloke",
    "ivy-authentication-token": "id-of-ivy",
}

# Configuration
logger = CustomLogger(log_level="INFO")


# Helper Functions
def get_user_id_with_authentication_header(authorization_header: Optional[str]) -> str:
    if (
        authorization_header
        and authorization_header.startswith("Bearer ")
        and (token := authorization_header[len("Bearer ") :].strip()) in AUTHORIZATION_TOKEN_TO_USER_ID_MAPPING
    ):
        return AUTHORIZATION_TOKEN_TO_USER_ID_MAPPING[token]
    raise HTTPException(status_code=401, detail="Unauthorized")
