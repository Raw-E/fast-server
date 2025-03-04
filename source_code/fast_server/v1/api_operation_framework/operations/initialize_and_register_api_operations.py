import importlib.util
import inspect
from pathlib import Path
import sys

from fastapi import FastAPI

from foundation.v1 import CustomLogger, Operation

from .api_operation import APIOperation
from ...utilities.logging_related import log_backend_routes

logger = CustomLogger(log_level="INFO")


class PathManager:
    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.path.pop(0)


class InitializeAndRegisterAPIOperations(Operation):
    def __init__(self, fastapi_app: FastAPI, api_operations_folder: Path):
        self.fastapi_app = fastapi_app
        self.api_operations_folder = api_operations_folder

    def _import_operations(self, base_path: str, target_folder: Path):
        operations = {}
        for py_file in target_folder.rglob("*.py"):
            if py_file.stem == "__init__":
                continue
            relative_parts = py_file.relative_to(target_folder).with_suffix("").parts
            module_name = f"{base_path}." + ".".join(relative_parts)
            spec = importlib.util.spec_from_file_location(module_name, str(py_file))
            if not (spec and spec.loader):
                continue
            try:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, APIOperation) and obj is not APIOperation:
                        operations[name] = obj
            except Exception as exc:
                logger.error(f"Error importing {module_name}: {exc}", stack_level=3)
        return operations

    def _register_operations(self, app: FastAPI, operations: dict):
        for op_cls in operations.values():
            op_instance = op_cls()
            method = getattr(app, op_instance.METHOD.lower(), None)
            if not method:
                continue
            try:
                method(
                    op_instance.ENDPOINT_PATH,
                    name=op_instance.__class__.__name__,
                    dependencies=op_instance.dependencies,
                    response_model=op_instance.RESPONSE_SCHEMA,
                )(op_instance.execute)
            except Exception as exc:
                logger.error(f"Failed to register {op_cls.__name__}: {exc}")

    async def execute(self) -> None:
        parent_path = str(self.api_operations_folder.parents[3])
        base_module_path = ".".join(
            self.api_operations_folder.relative_to(self.api_operations_folder.parents[3]).parts
        )
        with PathManager(parent_path):
            discovered_ops = self._import_operations(base_module_path, self.api_operations_folder)
            self._register_operations(self.fastapi_app, discovered_ops)

            from ...test.api_operations.get_health import GetHealth
            from ...test.api_operations.save_idea import SaveIdeaApiOperation

            explicit_ops = {
                "SaveIdeaApiOperation": SaveIdeaApiOperation,
                "GetHealth": GetHealth,
            }
            self._register_operations(self.fastapi_app, explicit_ops)

            log_backend_routes(self.fastapi_app)
