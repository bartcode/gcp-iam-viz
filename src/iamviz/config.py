from dataclasses import dataclass

from google.cloud._helpers import _determine_default_project


@dataclass
class Config:
    database_url: str = "bolt://neo4j:gcpviz@localhost:7687"
    scope: str = f"projects/{_determine_default_project()}"
