from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipFrom,
    StructuredRel,
    One,
    RelationshipTo,
)


class Project(StructuredNode):
    name = StringProperty(unique_index=True)
    resources = RelationshipFrom("Resource", "PARENT")


class ProjectRelation(StructuredRel):
    scope = StringProperty()


class Member(StructuredNode):
    email = StringProperty(unique_index=True)


class PolicyBinding(StructuredRel):
    role = StringProperty()
    scope = StringProperty()


class Resource(StructuredNode):
    display_name = StringProperty()
    name = StringProperty(unique_index=True)
    description = StringProperty()
    asset_type = StringProperty()
    location = StringProperty()
    project = RelationshipFrom(
        "Project", "CONTAINS", model=ProjectRelation, cardinality=One
    )
    members = RelationshipTo("Member", "HAS_POLICY", model=PolicyBinding)


# Project -> Policies
# Project -> Resources
# Member -> Role (-> Permissions)
# Member = user/group/service account

# MATCH q=(p:Project)-[:CONTAINS]->(r:Resource)-[hp:HAS_POLICY]->(m:Member) RETURN q
