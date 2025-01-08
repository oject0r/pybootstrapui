import os
import shutil
from pybootstrapui.desktop.build import start
from pybootstrapui import templates
import sys
from pathlib import Path
import platform
import urllib.request
import argparse
import tarfile
import zipfile


# Links for NW.js downloads
OFFICIAL_LINKS = {
    "windows_x64": "https://dl.nwjs.io/v0.94.1/nwjs-v0.94.1-win-x64.zip",
    "linux_x64": "https://dl.nwjs.io/v0.94.1/nwjs-v0.94.1-linux-x64.tar.gz",
    "macos_x64": "https://dl.nwjs.io/v0.94.1/nwjs-v0.94.1-osx-x64.zip",
    "windows_x86": "https://dl.nwjs.io/v0.94.1/nwjs-v0.94.1-win-ia32.zip",
    "linux_x86": "https://dl.nwjs.io/v0.94.1/nwjs-v0.94.1-linux-ia32.tar.gz",
    "macos_arm64": "https://dl.nwjs.io/v0.94.1/nwjs-v0.94.1-osx-arm64.zip",
}

OFFICIAL_SDK_LINKS = {
    "windows_x64": "https://dl.nwjs.io/v0.94.1/nwjs-sdk-v0.94.1-win-x64.zip",
    "linux_x64": "https://dl.nwjs.io/v0.94.1/nwjs-sdk-v0.94.1-linux-x64.tar.gz",
    "macos_x64": "https://dl.nwjs.io/v0.94.1/nwjs-sdk-v0.94.1-osx-x64.zip",
    "windows_x86": "https://dl.nwjs.io/v0.94.1/nwjs-sdk-v0.94.1-win-ia32.zip",
    "linux_x86": "https://dl.nwjs.io/v0.94.1/nwjs-sdk-v0.94.1-linux-ia32.tar.gz",
    "macos_arm64": "https://dl.nwjs.io/v0.94.1/nwjs-sdk-v0.94.1-osx-arm64.zip",
}

MIRROR_LINKS = {
    "windows_x64": "http://076s.space:9987/files/pybootstrap/nwjs-v0.94.1-win-x64.zip",
    "linux_x64": "http://076s.space:9987/files/pybootstrap/nwjs-v0.94.1-linux-x64.tar.gz",
    "macos_x64": "http://076s.space:9987/files/pybootstrap/nwjs-v0.94.1-osx-x64.zip",
    "windows_x86": "http://076s.space:9987/files/pybootstrap/nwjs-v0.94.1-win-ia32.zip",
    "linux_x86": "http://076s.space:9987/files/pybootstrap/nwjs-v0.94.1-linux-ia32.tar.gz",
    "macos_arm64": "http://076s.space:9987/files/pybootstrap/nwjs-v0.94.1-osx-arm64.zip",
}

MIRROR_SDK_LINKS = {
    "windows_x64": "http://076s.space:9987/files/pybootstrap/nwjs-sdk-v0.94.1-win-x64.zip",
    "linux_x64": "http://076s.space:9987/files/pybootstrap/nwjs-sdk-v0.94.1-linux-x64.tar.gz",
    "macos_x64": "http://076s.space:9987/files/pybootstrap/nwjs-sdk-v0.94.1-osx-x64.zip",
    "windows_x86": "http://076s.space:9987/files/pybootstrap/nwjs-sdk-v0.94.1-win-ia32.zip",
    "linux_x86": "http://076s.space:9987/files/pybootstrap/nwjs-sdk-v0.94.1-linux-ia32.tar.gz",
    "macos_arm64": "http://076s.space:9987/files/pybootstrap/nwjs-sdk-v0.94.1-osx-arm64.zip",
}


def download_file(url, dest_folder):
    """Download a file with progress bar without
    external libraries."""
    os.makedirs(dest_folder, exist_ok=True)
    file_name = os.path.join(dest_folder, url.split("/")[-1])

    with urllib.request.urlopen(url) as response:
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 1024

        with open(file_name, "wb") as file:
            print(f"Downloading {file_name}:")
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                file.write(chunk)
                downloaded += len(chunk)
                percent = downloaded * 100 // total_size if total_size else 0
                progress = (
                    f"[{'=' * (percent // 2)}{'-' * (50 - percent // 2)}] {percent}%"
                )
                print(progress, end="\r")

    print(f"\nFile downloaded to {file_name}")
    return Path(str(file_name)).absolute()


def get_system_info():
    """Detect system type and architecture."""
    # Determine OS type
    if sys.platform.startswith("win"):
        os_type = "windows"
    elif sys.platform.startswith("linux"):
        os_type = "linux"
    elif sys.platform.startswith("darwin"):
        os_type = "macos"
    else:
        os_type = "unknown"

    # Determine architecture
    machine = platform.machine().lower()
    if machine in ["amd64", "x86_64"]:
        arch = "x64"
    elif machine in ["i386", "i686", "x86"]:
        arch = "x86"
    elif "arm" in machine:
        arch = "arm64" if "64" in machine else "arm"
    else:
        arch = "unknown"

    return os_type, arch


def extract_archive(archive_path: str, dest_folder: str):
    """Automatically extracts a ZIP or TAR.GZ
    archive to the specified destination folder.

    If the archive contains only one top-level
    folder, its contents are extracted directly.
    :param archive_path: Path to the archive
        file.
    :type archive_path: str
    :param dest_folder: Destination folder for
        extraction.
    :type dest_folder: str
    """
    archive_path = Path(archive_path)
    dest_folder = Path(dest_folder)
    dest_folder.mkdir(parents=True, exist_ok=True)

    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    temp_extract_folder = dest_folder / "temp_extract"
    temp_extract_folder.mkdir(exist_ok=True)

    # Determine archive type and extract
    if archive_path.suffix == ".zip":
        with zipfile.ZipFile(archive_path, "r") as archive:
            archive.extractall(temp_extract_folder)
    elif archive_path.suffix == ".gz" and archive_path.name.endswith(".tar.gz"):
        with tarfile.open(archive_path, "r:gz") as archive:
            archive.extractall(temp_extract_folder)
    else:
        raise ValueError("Unsupported archive format. Supported formats: ZIP, TAR.GZ")

    # Handle single top-level folder
    extracted_items = list(temp_extract_folder.iterdir())
    if len(extracted_items) == 1 and extracted_items[0].is_dir():
        # Move contents of the single folder to the destination
        for item in extracted_items[0].iterdir():
            target_path = dest_folder / item.name
            if item.is_file():
                item.rename(target_path)
            elif item.is_dir():
                os.rename(item, target_path)
        extracted_items[0].rmdir()  # Remove the now-empty single folder
    else:
        # Move all extracted content directly to destination
        for item in extracted_items:
            target_path = dest_folder / item.name
            if item.is_file():
                item.rename(target_path)
            elif item.is_dir():
                os.rename(item, target_path)

    # Remove temporary folder
    temp_extract_folder.rmdir()
    print(f"Archive extracted successfully to: {dest_folder}")


def download_nwjs(source, version, dest_folder):
    """Download NW.js based on user's choice of
    source."""
    os_type, arch = get_system_info()
    key = f"{os_type}_{arch}"

    if version == "normal" and source == "mirror" and key in MIRROR_LINKS:
        print("Using mirror link for download.")
        return download_file(MIRROR_LINKS[key], dest_folder)
    elif version == "normal" and source == "official" and key in OFFICIAL_LINKS:
        print("Using official link for download.")
        return download_file(OFFICIAL_LINKS[key], dest_folder)
    elif version == "sdk" and source == "mirror" and key in MIRROR_SDK_LINKS:
        print("Using mirror link for download.")
        return download_file(MIRROR_SDK_LINKS[key], dest_folder)
    elif version == "sdk" and source == "official" and key in OFFICIAL_SDK_LINKS:
        print("Using official link for download.")
        return download_file(OFFICIAL_SDK_LINKS[key], dest_folder)
    else:
        print(
            f"No valid download link found for your platform.\nYour platform: {key}\n\nSupported platforms: {'\n'.join(MIRROR_LINKS.keys())}"
        )


def download(path_to_nwjs: Path):
    """Download NW.js to the specified
    directory."""

    print("Which source would you like to use for download?")
    print("1. Official NW.js website (slow download, more reliable)")
    print("2. Mirror server (faster download, less reliable)")

    user_choice = input("Enter your choice (1/2): ")
    source = "mirror" if user_choice == "2" else "official"

    print("Which version of NW.js would you like to download?")
    print("1. Normal version")
    print("2. SDK version")

    user_choice = input("Enter your choice (1/2): ")
    version = "sdk" if user_choice == "2" else "normal"

    zip_path = download_nwjs(source, version, str(path_to_nwjs))

    if not zip_path:
        return

    extract_archive(str(zip_path), str(path_to_nwjs))

    os.remove(zip_path)

    print(
        f"Downloading and extraction complete. Check your NW.js binaries at {str(path_to_nwjs.absolute())}"
    )


def create_project(project_path: Path):
    """Create a new NW.js project with system-
    specific configurations.

    Parameters:
        - project_path (Path): Path where the project will be created.
    """
    project_path.mkdir(parents=True, exist_ok=True)
    print("Creating your project...")

    # Read the default project template
    with open(templates.InternalTemplates.ProjectFile, "r", encoding="utf-8") as f:
        default_project = f.read()

    # System-specific NW.js path replacements
    os_type, _ = get_system_info()
    nwjs_paths = {
        "windows": r"nwjs\\nw.exe",
        "linux": r"nwjs/nw",
        "macos": "nwjs/nwjs.app/Contents/MacOS/nwjs",
    }

    if os_type in nwjs_paths:
        default_project = default_project.replace("path/to/nwjs", nwjs_paths[os_type])

    default_project = default_project.replace(
        "Project Name",
        (
            project_path.name.capitalize()
            if not project_path.name[0].isupper()
            else project_path.name
        ),
    )

    build_file_path = project_path / "config.zc"

    with build_file_path.open("w+", encoding="utf-8") as f:
        f.write(
            f"""
pybootstrapui {{
    project_name {project_path.name.capitalize() if not project_path.name[0].isupper() else project_path.name}
    
    main_file main.py
    nwjs_directory nwjs  # enter relative paths from project root only
    
    compiling_method PackNWjs  # either PackNWjs or ExternalNWjs.
    # If PackNWjs doesn't work for you, switch to ExternalNWjs.
    # Enter anything, but PackNWjs or ExternalNWjs if you want to pack NW.js custom way.
    
}}

pyinstaller_args ["--onefile", "--windowed"]

""".strip(
                "\n"
            )
        )

    # Write the final project file
    main_file_path = project_path / "main.py"
    with main_file_path.open("w+", encoding="utf-8") as f:
        f.write(default_project)

    print("Would you like to:")
    print("1. Copy an existing NW.js installation")
    print("2. Download a new NW.js version")

    user_input = input("Enter your choice (1/2): ").strip()

    if user_input == "1":
        handle_existing_nwjs(project_path)
    elif user_input == "2":
        download(project_path / "nwjs")
    else:
        print("Invalid choice. Please run the command again.")

    print(f"Project is ready!\nCheck your project at {project_path.absolute()}")


def handle_existing_nwjs(project_path: Path):
    """Handle copying an existing NW.js
    installation.

    Parameters:
        - project_path (Path): Path where NW.js will be copied.
    """
    while True:
        nwjs_exist = input(
            'Enter your NW.js directory (or type "quit" to exit): '
        ).strip()
        if nwjs_exist.lower() == "quit":
            quit()
        if Path(nwjs_exist).exists():
            shutil.copytree(nwjs_exist, project_path / "nwjs")
            print("NW.js copied successfully.")
            break
        print("Directory doesn't exist! Please try again.")


def parse_args():
    """Parse command-line arguments and execute
    the appropriate function."""
    parser = argparse.ArgumentParser(
        description="Utility for building and downloading NW.js projects."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: build
    build_parser = subparsers.add_parser(
        "build",
        help="Build the project with the specified PyBootstrapUI project. (WIP)",
    )
    build_parser.add_argument(
        "project_path",
        type=str,
        help="Path to the PyBootstrapUI project.",
        default="./",
    )

    # Subcommand: download
    download_parser = subparsers.add_parser(
        "download", help="Download NW.js to the specified directory."
    )
    download_parser.add_argument(
        "path_to_nwjs", type=str, help="Path to the directory for downloading NW.js."
    )

    project_parser = subparsers.add_parser(
        "create", help="Create a new PyBootstrapUI desktop project."
    )
    project_parser.add_argument(
        "project_path", type=str, help="Path where project is going to be."
    )

    args = parser.parse_args()

    if args.command == "build":
        print(
            "Warning: Building PyBootstrapUI apps is beta feature. There may be some bugs, but not much of them.\nYou can build projects that was generated by pybootstrapui create"
        )
        start(args.project_path)

    elif args.command == "download":
        path_to_nwjs = Path(args.path_to_nwjs)
        path_to_nwjs.mkdir(parents=True, exist_ok=True)

        download(path_to_nwjs)

    elif args.command == "create":
        path_to_project = Path(args.project_path)
        path_to_project.mkdir(parents=True, exist_ok=True)

        create_project(path_to_project)

    else:
        parser.print_help()


if __name__ == "__main__":
    parse_args()
