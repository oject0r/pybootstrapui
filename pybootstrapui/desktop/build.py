import os
from PyInstaller.__main__ import run as pyi_run
import sys
from pathlib import Path
from pybootstrapui import zeroconfig
from pybootstrapui.templates import InternalTemplates
import shutil


def start(project_path: str | Path):
    """Start function."""
    # Ensure project_path is a Path object
    project_path = Path(project_path)

    # Check if the configuration file exists
    if not project_path.joinpath("config.zc").exists():
        print(
            'Invalid project! No "config.zc" found. Try to re-create the project or create new config.zc'
        )
        sys.exit(1)

    # Load the configuration file
    configer = zeroconfig.Configer()
    config = configer.load_sync(str(project_path / "config.zc"))

    # Validate the presence of the 'pybootstrapui' key in the config
    if "pybootstrapui" not in config:
        print('Invalid config! No "pybootstrapui" nest found!')
        sys.exit(1)

    # Ensure required keys exist in the 'pybootstrapui' section
    if not all(
        key in config["pybootstrapui"]
        for key in ["main_file", "nwjs_directory", "compiling_method"]
    ):
        print('Invalid config! Missing required keys in "pybootstrapui" nest.')
        sys.exit(1)

    # Get the project name even if it's not in config.
    project_name = config["pybootstrapui"].get(
        "project_name", project_path.name.capitalize()
    )

    # Get the main file path from the configuration
    main_file_path = project_path.absolute() / config["pybootstrapui"]["main_file"]

    # Determine the correct separator for '--add-data' based on the operating system
    data_separator = ";" if os.name == "nt" else ":"
    nwjs_directory = config["pybootstrapui"]["nwjs_directory"]

    add_data_option = ""
    if config["pybootstrapui"]["compiling_method"].lower() == "packnwjs":
        add_data_option = f"--add-data={str(project_path.absolute() / nwjs_directory)}{data_separator}{nwjs_directory}"

    # Pack the library templates inside the _MEIPASS
    pack_templates_option = f"--add-data={InternalTemplates.TemplatesFolder}{data_separator}pybootstrapui/templates"
    pack_config_option = f"--add-data={str(project_path.absolute() / 'config.zc')}{data_separator}config.zc"

    # Retrieve additional PyInstaller arguments from the configuration
    additional_args = config.get("pyinstaller_args", [])
    pyi_args = [
        "--name",
        project_name,  # Set the output executable name
        "--distpath",
        f"{project_name}_compiled",  # Output directory for the final executable
        "--workpath",
        f"{project_name}_cache",  # Directory for temporary build files
        "--log-level=WARN",  # Set the log level to WARN
        pack_templates_option,  # Add templates for built programs to work
        pack_config_option,
        str(main_file_path),  # Path to the main script (should always be last)
    ] + additional_args

    if add_data_option:
        pyi_args.insert(4, add_data_option)

    pyi_run(pyi_args)

    if config["pybootstrapui"]["compiling_method"].lower() == "externalnwjs":
        shutil.copytree(
            project_path.absolute() / nwjs_directory,
            os.path.join(f"{project_name}_compiled", nwjs_directory),
            dirs_exist_ok=True,
        )

    print(
        f'Successfully compiled your project "{project_name}"!\n'
        f'You can find the binaries in the "{project_name}_compiled" folder.\n'
        f'It is safe to delete the build cache in "{project_name}_cache", but keep in mind '
        f"that the next build will take as long as the first one."
    )
