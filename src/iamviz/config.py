"""Base configuration."""
from dataclasses import dataclass

from google.cloud._helpers import _determine_default_project


@dataclass
class Config:
    """Configuration class for database and GCP project."""

    database_url: str = "bolt://neo4j@localhost:7687"
    project_id: str = _determine_default_project()
