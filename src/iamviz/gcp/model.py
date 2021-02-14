"""Base Neomodel definitions."""
from neomodel import (
    StructuredNode,
    StringProperty,
    StructuredRel,
    RelationshipFrom,
)


class ProjectRelation(StructuredRel):
    """Relationship between an asset an a project."""

    scope = StringProperty()


class Member(StructuredNode):
    """Users/members reference."""

    email = StringProperty(unique_index=True)


class PolicyBinding(StructuredRel):
    """Relationship that describes the policy bindings from a user on a resource."""

    role = StringProperty()
    scope = StringProperty()


class Project(StructuredNode):
    """Base project node."""

    name = StringProperty(unique_index=True)
    displayName = StringProperty()
    assetUrl = StringProperty()
    description = StringProperty()
    assetType = StringProperty()
    location = StringProperty()
    members = RelationshipFrom(Member, "HAS_POLICY", model=PolicyBinding)
