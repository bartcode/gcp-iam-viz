from iamviz.gcp.assets import retrieve_iam_policies
from iamviz.gcp.asset import IamPolicyRecord


def test_retrieve_gcp_assets():

    for asset in assets:
        assert isinstance(asset, IamPolicyRecord)


