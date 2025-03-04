import os
import subprocess
import time

from foundation.v1 import CustomLogger

logger = CustomLogger(log_level="INFO")


def get_server_port() -> int:
    port_string = os.getenv("FASTAPI_SERVER_PORT")
    if not port_string:
        raise ValueError("FASTAPI_SERVER_PORT not set!")

    try:
        port = int(port_string)
        free_up_port(port)
        return port
    except Exception as error:
        raise Exception(f"Port {port_string} can't be used: {error}")


def free_up_port(port: int) -> None:
    result = subprocess.run(f"lsof -i :{port} -t", shell=True, capture_output=True, text=True)

    if result.stdout:
        subprocess.run(f"kill -9 {' '.join(result.stdout.strip().split())}", shell=True)
        time.sleep(1)
