"""Methods that help save Storage IAM policies."""
import logging
from typing import Type

from google.cloud import storage
from neomodel import StructuredNode

from iamviz.gcp.model import Member

logger = logging.getLogger(__name__)


def save_storage_iam_policies(
    project: str, model: Type[StructuredNode], scope: str
) -> None:
    """
    Retrieve all buckets and their respective IAM policies.
    :param project: Project node
    :param model: Model to use for saving the bucket nodes.
    :param scope: Scope
    :return: None
    """
    client = storage.Client(project=project)
    buckets = [b for b in client.list_buckets()]

    for bucket in buckets:
        logger.info("Loading bucket: %s", bucket)
        bucket_model = model.get_or_create(
            dict(
                name=bucket.name,
                assetUrl=f"//storage.googleapis.com/{bucket.name}",
                displayName=bucket.name,
                description="",
                assetType="storageBucket",
                location=bucket.location.lower(),
            )
        )[0]

        for binding in bucket.get_iam_policy().to_api_repr().get("bindings", []):
            for member_email in binding.get("members", []):
                logger.info(
                    "Settings policy %s on bucket %s to %s",
                    binding["role"],
                    bucket.name,
                    member_email,
                )
                member = Member.get_or_create(dict(email=member_email))[0]

                relationship = bucket_model.members.connect(member)
                relationship.role = binding["role"]
                relationship.scope = scope
                relationship.save()
