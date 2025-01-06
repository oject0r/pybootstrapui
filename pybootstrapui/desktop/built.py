import sys
import os
from pybootstrapui import zeroconfig
from pathlib import Path
from pybootstrapui.__main__ import get_system_info


def resource_path(relative_path: str) -> str:
    """Get absolute path to a resource,
    compatible with both development and
    PyInstaller environments.

    Parameters:
        - relative_path (str): Relative path to the resource.
    :return: Absolute path to the resource.
    :rtype: - str
    """
    try:
        # If running as a bundled application (PyInstaller)
        base_path = sys._MEIPASS
    except AttributeError:
        # If running in a development environment
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Load configuration file
try:
    config = zeroconfig.Configer().load_sync(resource_path("config.zc"))
except OSError:
    config = zeroconfig.Configer().load_sync(resource_path("config.zc/config.zc"))

# Get system information
os_type, arch = get_system_info()

# Define platform-specific NW.js paths
nwjs_paths = {
    "windows": r"nw.exe",
    "linux": r"nw",
    "macos": "nwjs.app/Contents/MacOS/nwjs",
}

# Determine NW.js executable path
NWJSPath = ""

# First, check if NW.js exists in the development environment
nwjs_dev_path = (
    Path(os.getcwd())
    .parent.absolute()
    .joinpath(config["pybootstrapui"]["nwjs_directory"])
)

if nwjs_dev_path.exists():
    NWJSPath = nwjs_dev_path / nwjs_paths[os_type]

# If not found, check in the bundled PyInstaller environment
else:
    nwjs_resource_path = Path(resource_path(config["pybootstrapui"]["nwjs_directory"]))
    if nwjs_resource_path.exists():
        NWJSPath = nwjs_resource_path / nwjs_paths[os_type]
