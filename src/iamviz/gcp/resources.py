import logging
from typing import Type, Dict

from google.cloud import asset
from iamviz.gcp.mappings import strip_asset_type
from neomodel import db, clear_neo4j_database, StructuredNode

logger = logging.getLogger(__name__)


def clear_resources(scope: str) -> None:
    logger.info("Clearing resources linked to scope %s", scope)
    clear_neo4j_database(db)


def get_project_resource(
    client: asset.AssetServiceClient, asset_types: Dict[str, type], scope: str
) -> Type[StructuredNode]:
    logger.info("Searching for Project node.")
    projects = client.search_all_resources(
        scope=scope, asset_types=["cloudresourcemanager.googleapis.com/Project"]
    )

    for search_result in projects:  # Should only be one.
        logger.info("Found Project node.")

        return asset_types["cloudresourcemanagerProject"](
            # name=f"{asset_type}/{resource.display_name}",
            name=search_result.display_name,
            assetUrl=search_result.name,
            displayName=search_result.display_name,
            description=search_result.description,
            assetType=search_result,
            location=search_result.location,
        ).save()

    raise LookupError("Unable to find project node.")


def save_all_resources(
    client: asset.AssetServiceClient,
    asset_types: Dict[str, type],
    project: Type[StructuredNode],
    scope: str,
) -> Dict[str, Type[StructuredNode]]:
    logger.info("Searching all resources within scope %s.", scope)

    results: Dict[str, Type[StructuredNode]] = {}

    for resource in client.search_all_resources(scope=scope):
        if resource.asset_type == "cloudresourcemanager.googleapis.com/Project":
            results[resource.name] = project
            continue

        logger.info("Found resource %s (%s).", resource.name, resource.asset_type)

        try:
            asset_type = strip_asset_type(resource.asset_type)

            node = asset_types[asset_type](
                # name=f"{asset_type}/{resource.display_name}",
                name=resource.display_name,
                assetUrl=resource.name,
                displayName=resource.display_name,
                description=resource.description,
                assetType=asset_type,
                location=resource.location.lower(),
            )

            node.save()

            relationship = node.project.connect(project)
            relationship.scope = scope
            relationship.save()

            results[resource.name] = node
        except KeyError:
            logger.warning(
                "Unable to add resource %s, as it's not a searchable asset.",
                resource.asset_type,
            )

    return results
