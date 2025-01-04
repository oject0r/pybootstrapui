import json
import os
import subprocess
import tempfile
import shutil
from pathlib import Path


class InvalidIconFile(Exception):
    """
    Custom exception raised when an invalid icon file is provided.

    Attributes:
            - `message` (str): Error message describing the issue.
    """


def run_page_in_desktop(
    page,
    nwjs_path,
    icon: str | None = None,
    title="NW.js App",
    width=800,
    height=600,
    resizable=True,
):
    """
    Renders a `Page` instance and launches it in NW.js.

    Parameters:
            - `page` (Page): Instance of the Page class to render.
            - `nwjs_path` (str): Path to the NW.js executable.
            - `title` (str): Title of the NW.js window (default: "NW.js App").
            - `width` (int): Width of the NW.js window (default: 800).
            - `height` (int): Height of the NW.js window (default: 600).
            - `icon` (str | None): Path to the icon file (optional, must be PNG if provided).
            - `resizable` (bool): Whether the NW.js window is resizable (default: True).

    Raises:
            - `FileNotFoundError`: If NW.js executable or icon file is not found.
            - `InvalidIconFile`: If the icon file is not a PNG.

    Example:
            # Launch a page in NW.js with a custom icon and dimensions
            ```
            run_page_in_desktop(
                    page=page_instance,
                    nwjs_path="/path/to/nwjs",
                    icon="/path/to/icon.png",
                    title="My NW.js App",
                    width=1024,
                    height=768,
                    resizable=False
            )
            ```

    Note:
            - A temporary directory is created to store `main.html` and `package.json`.
            - The directory is removed after the NW.js application is closed.
    """

    # Create a temporary directory for NW.js application files
    directory = tempfile.mkdtemp(prefix="PyBootstrapUI")

    # Save the page's compiled HTML into a file
    with open(os.path.join(directory, "main.html"), "w+", encoding="utf-8") as f:
        f.write(page.compile())

    # Handle the optional icon
    if icon:
        path_icon = Path(icon)

    # Build the `package.json` file for NW.js
    package_data = build_package_json(
        title, width, height, icon=path_icon.name if icon else None, resizable=resizable
    )

    # Save the `package.json` file
    with open(os.path.join(directory, "package.json"), "w+", encoding="utf-8") as file:
        file.write(json.dumps(package_data))

    # Validate NW.js path
    if not os.path.exists(nwjs_path):
        raise FileNotFoundError(f"NW.js executable not found at {nwjs_path}")

    # Validate icon file
    if icon:
        if not icon.endswith(".png"):
            raise InvalidIconFile("Icon files MUST be PNG!")
        if not os.path.exists(icon):
            raise FileNotFoundError(f"Icon file not found at {icon}")
        shutil.copy(icon, os.path.join(directory, path_icon.name))

    # Run the NW.js application
    subprocess.run([nwjs_path, directory])

    # Clean up temporary files
    shutil.rmtree(directory)


def build_package_json(
    title: str,
    width: int = 800,
    height: int = 600,
    *,
    resizable: bool = True,
    name: str = "nwjs-app",
    icon: str | None = None,
    version: str = "1.0.0",
    description: str = "A NW.js application",
) -> dict[str, str | dict[str, str | bool]]:
    """
    Builds a `package.json` dictionary for NW.js configuration.

    Parameters:
            - `title` (str): Title of the NW.js application window.
            - `width` (int): Width of the application window (default: 800).
            - `height` (int): Height of the application window (default: 600).
            - `resizable` (bool): Whether the window is resizable (default: True).
            - `name` (str): Name of the application (default: "nwjs-app").
            - `icon` (str | None): Path to the application icon (optional).
            - `version` (str): Version of the application (default: "1.0.0").
            - `description` (str): Description of the application (default: "A NW.js application").

    Returns:
            - dict: The configuration dictionary for `package.json`.

    Example:
            # Create a package.json configuration
            ```
            package_json = build_package_json(
                    title="My App",
                    width=1024,
                    height=768,
                    resizable=False,
                    name="my-nwjs-app",
                    icon="icon.png"
            )
            ```

    Note:
            - This function includes default Chromium arguments for media playback
              and disabled user gesture requirements.
    """

    return {
        "name": name,
        "version": version,
        "description": description,
        "main": "main.html",
        "window": {
            "title": title,
            "icon": str(icon) if icon else "",
            "width": width,
            "height": height,
            "resizable": resizable,
        },
        "chromium-args": "--disable-user-media-security --allow-hidden-media-playback --autoplay-policy=no-user-gesture-required",
    }
