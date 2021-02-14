"""GCP IAM Viz helps to visualise IAM policies in Neo4j. This is the entrypoint of the CLI."""
import argparse
import logging
import os

from google.cloud import asset

from iamviz.config import Config
from iamviz.gcp.assets import get_gcp_asset_models
from iamviz.gcp.iam_policies import save_all_iam_policies
from iamviz.gcp.resources import (
    clear_resources,
    save_all_resources,
    get_project_resource,
)
from iamviz.gcp.storage import save_storage_iam_policies

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    """Entrypoint method which runs the (very small) ETL pipeline."""
    parser = argparse.ArgumentParser(description="GCP IAM loader.")
    parser.add_argument(
        "--project_id",
        "-p",
        dest="project",
        type=str,
        default=Config.project_id,
    )
    parser.add_argument(
        "--database-url",
        "-d",
        type=str,
        default=Config.database_url,
    )

    arguments, _ = parser.parse_known_args()

    scope = f"projects/{arguments.project}"

    client = asset.AssetServiceClient()

    # Clear database. (Yes, this is ugly.)
    clear_resources()

    logger.info("Scope: %s", scope)
    # Determine which asset types are available.
    # Models will be created for all of them.
    asset_types = get_gcp_asset_models()

    # Create project node.
    project = get_project_resource(client, asset_types, scope)

    # Save all resources and list them under the project node.
    resources = save_all_resources(client, asset_types, project, scope)

    # Save all IAM policies.
    save_all_iam_policies(client, resources, scope)

    # Since policies on Google Cloud Storage are not properly available,
    # use the Cloud Storage API to retrieve IAM policies.
    save_storage_iam_policies(
        project=os.path.basename(scope),
        model=asset_types["storageBucket"],
        scope=scope,
    )


if __name__ == "__main__":
    main()
