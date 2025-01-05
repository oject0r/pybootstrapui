"""
This thing is utility only and should be used when commiting into a branch
"""

import re
import os


def remove_backticks_in_multiline_comments(code: str) -> str:
	"""
	Removes all '' symbols from multi-line comments enclosed in triple quotes.
	"""

	def replacer(match):
		return match.group(0).replace('`', '')

	return re.sub(r'("""[\s\S]*?""")', replacer, code)


def process_files_in_directory(directory: str):
	"""
	Recursively processes all Python files in the given directory,
	removing '' from multi-line comments.
	"""
	for root, _, files in os.walk(directory):
		for file in files:
			if file.endswith('.py'):
				file_path = os.path.join(root, file)
				try:
					with open(file_path, 'r', encoding='utf-8') as f:
						content = f.read()

					# Обновляем содержимое файла
					updated_content = remove_backticks_in_multiline_comments(content)

					# Сохраняем изменения
					with open(file_path, 'w', encoding='utf-8') as f:
						f.write(updated_content)

					print(f"[Processed] {file_path}")
				except Exception as e:
					print(f"[Error] Failed to process {file_path}: {e}")


if __name__ == "__main__":
	current_directory = os.getcwd()
	process_files_in_directory(current_directory)
