import os
from PyInstaller.__main__ import run
import shutil
import time

# In progress

def start(script_path: str, nw_js_path: str, additional_args: list[str]):
	pyi_args = [script_path, '--log-level=WARN'] + additional_args

	if not os.path.exists(nw_js_path):
		raise FileNotFoundError(f'No such folder {nw_js_path}!')

	shutil.copytree(nw_js_path, 'NodeWebkit', dirs_exist_ok=True)

	while not os.path.exists('NodeWebkit'):
		time.sleep(0.1)

	pyi_args.append('--add-data="NodeWebkit:NodeWebkit"')
	run(pyi_args)
