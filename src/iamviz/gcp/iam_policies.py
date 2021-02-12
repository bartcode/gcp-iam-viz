import logging
from typing import Dict, Type

from google.cloud import asset

from iamviz.gcp.model import Member
from neomodel import StructuredNode

logger = logging.getLogger(__name__)


def save_all_iam_policies(
    client: asset.AssetServiceClient,
    resources: Dict[str, Type[StructuredNode]],
    scope: str,
) -> None:
    logger.info("Searching all IAM policies within scope %s.", scope)

    for policy in client.search_all_iam_policies(scope=scope):
        resource = resources[policy.resource]

        for binding in policy.policy.bindings:
            for member_email in binding.members:
                logger.info(
                    "Found IAM policy %s on resource %s for user %s.",
                    binding.role,
                    policy.resource,
                    member_email,
                )
                member = Member.get_or_create(dict(email=member_email))[0]

                relationship = resource.members.connect(member)
                relationship.role = binding.role
                relationship.scope = scope
                relationship.save()
