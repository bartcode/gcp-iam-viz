import logging
from typing import List

from google.cloud import asset

from iamviz.gcp.model import Resource, Member

logger = logging.getLogger(__name__)


def save_all_iam_policies(client: asset.AssetServiceClient, scope: str) -> List[Member]:
    logger.info("Searching all IAM policies within scope %s.", scope)
    policies = []

    for policy in client.search_all_iam_policies(scope=scope):
        resource = Resource.nodes.first(name=policy.resource)

        for binding in policy.policy.bindings:
            for member_email in binding.members:
                logger.info(
                    "Found IAM policy %s on resource %s for user %s.",
                    binding.role,
                    binding.role,
                    member_email,
                )
                member = Member.get_or_create(dict(email=member_email))[0]

                relationship = resource.members.connect(member)
                relationship.role = binding.role
                relationship.scope = scope
                relationship.save()

                policies.append(member)

    return policies
