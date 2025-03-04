# THIS CODE HAS BEEN ORGANIZED

"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for idea_data_model.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Local Development Imports
from database_dimension.v1 import MongoDBBaseModel

from foundation.v1 import CustomLogger

# Configuration
logger = CustomLogger(log_level="INFO")


# Classes
class IdeaDataModel(MongoDBBaseModel):
    # Class attributes
    idea: str
    submitted_for: str