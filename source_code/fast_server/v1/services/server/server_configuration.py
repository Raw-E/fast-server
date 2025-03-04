from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel

from foundation.v1 import CustomLogger

from ...utilities.api_operations_path import find_api_operations_path
from ...utilities.port_related import get_server_port

logger = CustomLogger(log_level="INFO")


class ServerConfiguration(BaseModel):
    api_operations_path: Path
    host: str = "0.0.0.0"
    port: int
    reload: bool = True
    reload_dirs: List[str] = ["source_code"]

    @classmethod
    def create(cls, **kwargs) -> "ServerConfiguration":
        try:
            return cls(
                api_operations_path=find_api_operations_path(),
                port=get_server_port(),
                **kwargs,
            )
        except ValueError as e:
            logger.error(f"Failed to initialize server configuration: {e}")
            raise

    def to_uvicorn_configuration(self) -> Dict[str, Any]:
        return {
            "app": "fast_server.v1.services.server.server_runner:ServerRunner.create_server",
            "host": self.host,
            "port": self.port,
            "reload": self.reload,
            "reload_dirs": self.reload_dirs,
            "factory": True,
        }
