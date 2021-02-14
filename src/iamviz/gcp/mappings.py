"""Methods that map values from one to another. (Hah.)"""


def strip_asset_type(asset: str) -> str:
    """
    Removes the API url from the asset type, such that (for instance)
    the asset type storage.googleapis.com/Bucket becomes storageBucket.
    :param asset: Asset type URL.
    :return: Asset name.
    """
    return asset.replace(".googleapis.com/", "", 1).replace("k8s.io/", "k8s", 1)
