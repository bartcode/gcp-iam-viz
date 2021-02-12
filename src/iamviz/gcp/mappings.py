def strip_asset_type(asset: str) -> str:
    return asset.replace(".googleapis.com/", "", 1).replace("k8s.io/", "k8s")
