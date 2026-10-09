from pathlib import Path
import sys


def get_asset_path(relative_path):
    bundle_directory = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return str(Path(bundle_directory) / relative_path)
