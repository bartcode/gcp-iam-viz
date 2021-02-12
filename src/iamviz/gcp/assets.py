import logging
from pathlib import Path
from typing import Dict

import pkg_resources
import requests
from bs4 import BeautifulSoup
from neomodel import StructuredNode, RelationshipFrom, StringProperty, One

from iamviz import __package__ as _resource_dir
from iamviz.gcp.mappings import strip_asset_type
from iamviz.gcp.model import ProjectRelation, PolicyBinding, Member, Project

logger = logging.getLogger(__name__)


def get_gcp_asset_models() -> Dict[str, type]:
    cache_path = Path(
        _resource_dir,
        pkg_resources.resource_filename(_resource_dir, "cache/asset_types.tmp.html"),
    )

    if not cache_path.exists():
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(
            requests.get(
                "https://cloud.google.com/asset-inventory/docs/supported-asset-types"
            ).text
        )

    soup = BeautifulSoup(cache_path.read_text(), "html.parser")
    asset_types = [
        e.text
        for e in soup.select_one("#searchable_asset_types ~ table").select(
            "tr > td code"
        )
    ]

    classes = {}

    for asset in asset_types:
        if "/" not in asset:
            continue

        if asset == "cloudresourcemanager.googleapis.com/Project":
            classes["cloudresourcemanagerProject"] = Project
            continue

        asset_type = strip_asset_type(asset)

        logger.debug("Registering asset type: %s", asset_type)

        classes[asset_type] = type(
            asset_type,
            (StructuredNode,),
            {
                "displayName": StringProperty(),
                "assetUrl": StringProperty(default=asset),
                "name": StringProperty(unique_index=True),
                "description": StringProperty(),
                "assetType": StringProperty(),
                "location": StringProperty(),
                "project": RelationshipFrom(
                    Project, "CONTAINS", model=ProjectRelation, cardinality=One
                ),
                "members": RelationshipFrom(Member, "HAS_POLICY", model=PolicyBinding),
            },
        )

    return classes
