# THIS CODE HAS BEEN ORGANIZED

"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for test_importing_this_package.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports
import importlib
from importlib.util import find_spec

# Third-Party Imports
import pytest


# Main Functions
def test_importing_this_package():
    spec = find_spec("fast_server")
    assert spec is not None, "Package 'fast_server' not found!"

    try:
        importlib.import_module("fast_server")
    except ImportError as e:
        pytest.fail(f"Failed to import 'fast_server' package: {e}")
