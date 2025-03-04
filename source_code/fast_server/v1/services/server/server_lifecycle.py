from contextlib import asynccontextmanager

from fastapi import FastAPI

from .server_configuration import ServerConfiguration
from ...api_operation_framework.operations.initialize_and_register_api_operations import (
    InitializeAndRegisterAPIOperations,
)


@asynccontextmanager
async def server_lifecycle(server: FastAPI, configuration: ServerConfiguration):
    await InitializeAndRegisterAPIOperations(server, configuration.api_operations_path)
    yield
