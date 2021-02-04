import logging
from typing import List

from google.cloud import asset
from neomodel import db, clear_neo4j_database

from iamviz.gcp.model import Project, Resource

logger = logging.getLogger(__name__)


def clear_resources(scope: str) -> None:
    logger.info("Clearing resources linked to scope %s", scope)
    clear_neo4j_database(db)


def save_all_resources(client: asset.AssetServiceClient, scope: str) -> List[Resource]:
    logger.info("Searching all resources within scope %s.", scope)

    results: List[Resource] = []

    for resource in client.search_all_resources(scope=scope):
        logger.info("Found resource %s (%s).", resource.name, resource.asset_type)
        project = Project.get_or_create(dict(name=resource.project))[0]

        node = Resource(
            name=resource.name,
            display_name=resource.display_name,
            description=resource.description,
            asset_type=resource.asset_type,
            location=resource.location,
        )

        node.save()

        relationship = node.project.connect(project)
        relationship.scope = scope
        relationship.save()

        results.append(node)

    return results
