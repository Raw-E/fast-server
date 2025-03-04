import inspect
from pathlib import Path
import sys


def find_api_operations_path() -> Path:
    """Find the path to the API operations directory.

    Returns:
        Path: The path to the API operations directory.

    Raises:
        ValueError: If the API operations directory is not found.
    """
    api_operations_path = Path(inspect.getfile(sys.modules["__main__"])).parent / "operations" / "api_operations"

    if not api_operations_path.exists():
        raise ValueError(f"API operations directory not found at: {api_operations_path}")

    return api_operations_path
