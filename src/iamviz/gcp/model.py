from neomodel import (
    StructuredNode,
    StringProperty,
    StructuredRel,
    RelationshipFrom,
)


class ProjectRelation(StructuredRel):
    scope = StringProperty()


class Member(StructuredNode):
    email = StringProperty(unique_index=True)


class PolicyBinding(StructuredRel):
    role = StringProperty()
    scope = StringProperty()


class Project(StructuredNode):
    name = StringProperty(unique_index=True)
    displayName = StringProperty()
    assetUrl = StringProperty()
    description = StringProperty()
    assetType = StringProperty()
    location = StringProperty()
    members = RelationshipFrom(Member, "HAS_POLICY", model=PolicyBinding)


# Project -> Policies
# Project -> Resources
# Member -> Role (-> Permissions)
# Member = user/group/service account

# MATCH q=(p:Project)-[:CONTAINS]->(r:Resource)-[hp:HAS_POLICY]->(m:Member) RETURN q
