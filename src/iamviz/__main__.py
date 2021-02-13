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

    clear_resources(scope)

    logger.info("Scope: %s", scope)
    asset_types = get_gcp_asset_models()

    project = get_project_resource(client, asset_types, scope)
    resources = save_all_resources(client, asset_types, project, scope)
    save_all_iam_policies(client, resources, scope)
    save_storage_iam_policies(
        project=os.path.basename(scope),
        model=asset_types["storageBucket"],
        scope=scope,
    )


if __name__ == "__main__":
    main()
