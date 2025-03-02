import os
import sys
from pathlib import Path
from pybootstrapui import zeroconfig
from pybootstrapui.templates import InternalTemplates
import shutil
import subprocess


def find_py_files(directory, py_files=None):
    if py_files is None:
        py_files = []

    try:
        for entry in os.scandir(directory):
            if entry.is_file() and entry.name.endswith('.py'):
                py_files.append(entry.path)
            elif entry.is_dir():
                find_py_files(entry.path, py_files)
    except PermissionError:
        pass
    except Exception as e:
        print(f"Error processing {directory}: {e}")

    return py_files


def obfuscate_with_pyarmor(script_path, output_dir):
    """
    Obfuscates a Python script using PyArmor.
    """
    if not os.path.exists(script_path):
        print(f"Error: File {script_path} not found.")
        return

    try:
        # Build the PyArmor command
        command = [
            "pyarmor", "obfuscate",
            "--output", output_dir,  # Specify the output directory
            script_path  # Path to the source script
        ]
        # Run the command
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while executing the command: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


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
    pack_config_option = f"--add-data={str(project_path.absolute() / "config.zc")}{data_separator}config.zc"

    obfuscate_code = config["pybootstrapui"].get("obfuscate_code", False)

    if obfuscate_code:
        try:
            import pyarmor  # PyArmor import check
        except ImportError:
            print(
                "FATAL: (code obfuscate) PyArmor package not found!\n"
                "Please install it via pip:\n"
                "pip install pyarmor\n"
                "Or disable code obfuscation in compiling config:\n"
                "obfuscate_code true —> obfuscate_code false"
            )
            sys.exit(1)

        print(
            "Code obfuscation is currently in beta.\n"
            "For better results, consider manually obfuscating the code.\n"
            "Code obfuscation may trigger antivirus, so proceed at your own risk."
        )

        # Create output directory for obfuscated files
        obf_dir = f"{project_name}_obf"
        if not os.path.exists(obf_dir):
            try:
                os.mkdir(obf_dir)
            except OSError as e:
                print(f"Error creating obfuscation directory '{obf_dir}': {e}")
                sys.exit(1)

        # Find all .py files in the project
        py_files = find_py_files(project_path)
        if not py_files:
            print("No .py files found in the project directory.")
            sys.exit(0)

        # Obfuscate each Python file
        for file in py_files:
            try:
                obfuscate_with_pyarmor(os.path.abspath(file), obf_dir)
            except Exception as e:
                print(f"Error obfuscating {file}: {e}")

        # Copy the main file to the obfuscated directory
        try:
            main_file_obf_path = os.path.join(obf_dir, os.path.basename(main_file_path))
            shutil.copy(main_file_path, main_file_obf_path)
        except Exception as e:
            print(f"Error copying main file to obfuscation directory: {e}")


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

    try:
        from PyInstaller.__main__ import run as pyi_run
    except ImportError:
        print(
            "FATAL: PyInstaller package not found!\n"
            "Please install it via pip:\n"
            "pip install pyinstaller"
        )
        sys.exit(1)

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
