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
    .absolute()
    .joinpath(config["pybootstrapui"]["nwjs_directory"])
)


def find_nwjs_binary(root_directory: str):
    binary_name = ""

    if os_type == "windows":
        binary_name = nwjs_paths["windows"]
    elif os_type == "linux":
        binary_name = nwjs_paths["linux"]
    elif os_type == "darwin":
        binary_name = nwjs_paths["macos"]
    else:
        raise ValueError(f"Unsupported platform: {os_type}")

    for root, dirs, files in os.walk(root_directory):
        if os_type == "macos":
            app_path = os.path.join(root, binary_name)
            if os.path.exists(app_path) and os.path.isfile(app_path):
                return app_path
        else:
            if binary_name in files:
                return os.path.join(root, binary_name)

    return None

if nwjs_dev_path.exists():
    NWJSPath = nwjs_dev_path / nwjs_paths[os_type]

# If not found, check in the bundled PyInstaller environment
else:
    nwjs_resource_path = Path(resource_path(config["pybootstrapui"]["nwjs_directory"]))
    if nwjs_resource_path.exists():
        NWJSPath = nwjs_resource_path / nwjs_paths[os_type]
    else:
        maybe_nwjs = find_nwjs_binary(os.getcwd())
        if maybe_nwjs:
            NWJSPath = maybe_nwjs

if not NWJSPath:
    print('WARNING: Could not find NW.js binaries.')