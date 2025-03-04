import os

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from .server_configuration import ServerConfiguration
from .server_lifecycle import server_lifecycle

# Configuration
load_dotenv(override=True)
FASTAPI_CONFIGURATION_ENV_KEY = "FASTAPI_APP_CONFIGURATION"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "development":
    load_dotenv(".env.development", override=True)
elif ENVIRONMENT == "production":
    load_dotenv(".env.production", override=True)


class ServerRunner:
    def __init__(self, configuration: ServerConfiguration):
        self.configuration = configuration
        os.environ[FASTAPI_CONFIGURATION_ENV_KEY] = self.configuration.model_dump_json()

    @classmethod
    def create_server(cls) -> FastAPI:
        config = ServerConfiguration.model_validate_json(os.environ[FASTAPI_CONFIGURATION_ENV_KEY])
        return FastAPI(lifespan=lambda server: server_lifecycle(server, config))

    def run(self) -> None:
        uvicorn.run(**self.configuration.to_uvicorn_configuration())
