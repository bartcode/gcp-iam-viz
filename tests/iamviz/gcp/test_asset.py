import pytest

from iamviz.gcp.asset import IamPolicyRecord


@pytest.mark.parametrize("record, result", [
    (IamPolicyRecord(project="test", resource="//cloudresourcemanager.googleapis.com/projects/playground-bart", role="roles/bigquery.viewer", member="user:test@test.com"), "cloudresourcemanager"),
    (IamPolicyRecord(project="test", resource="//cloudresourcemanager.googleapis.com", role="roles/bigquery.viewer", member="user:test@test.com"), "cloudresourcemanager"),
    (IamPolicyRecord(project="test", resource="//cloudresourcemanager.googleapis.com//test", role="roles/bigquery.viewer", member="user:test@test.com"), "cloudresourcemanager"),
])
def test_iam_policy_record_api(record: IamPolicyRecord, result: str):
    assert record.api == result
