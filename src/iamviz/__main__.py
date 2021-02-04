import argparse
import logging

from google.cloud import asset

from iamviz import Config
from iamviz.gcp.iam_policies import save_all_iam_policies
from iamviz.gcp.model import Resource, Member
from iamviz.gcp.resources import clear_resources, save_all_resources

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="GCP IAM loader.")
    parser.add_argument(
        "--scope",
        "-s",
        dest="scope",
        type=str,
        default=Config.scope,
    )
    parser.add_argument(
        "--database-url",
        "-d",
        type=str,
        default=Config.database_url,
    )

    arguments, _ = parser.parse_known_args()

    client = asset.AssetServiceClient()

    clear_resources(arguments.scope)

    logger.info("Scope: %s", arguments.scope)

    asset_methods = {
        Resource: save_all_resources,
        Member: save_all_iam_policies,
    }

    for asset_type, asset_saver in asset_methods.items():
        asset_saver(client, arguments.scope)


if __name__ == "__main__":
    main()
