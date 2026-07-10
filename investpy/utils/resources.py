"""Load an investpy registry CSV plus an optional isolated custom overlay.

The custom_<name>.csv overlay files hold hand-captured rows for instruments
absent from Investing.com's bulk registry exports. Keeping them in separate
files means an upstream registry refresh never clobbers our additions.
"""

import pandas as pd
import pkg_resources

_PACKAGE = "investpy"


def load_registry(filename):
    """Read resources/<filename>, overlaying resources/custom_<filename> if present.

    Rows sharing an `id` with a custom row are replaced by the custom row.
    """
    base_path = "/".join(("resources", filename))
    if not pkg_resources.resource_exists(_PACKAGE, base_path):
        raise FileNotFoundError(f"ERR#0060: {filename} not found or errored.")
    base = pd.read_csv(
        pkg_resources.resource_filename(_PACKAGE, base_path), keep_default_na=False
    )

    custom_path = "/".join(("resources", f"custom_{filename}"))
    if not pkg_resources.resource_exists(_PACKAGE, custom_path):
        return base
    custom = pd.read_csv(
        pkg_resources.resource_filename(_PACKAGE, custom_path), keep_default_na=False
    )
    merged = pd.concat([base, custom], ignore_index=True)
    return merged.drop_duplicates(subset=["id"], keep="last").reset_index(drop=True)
