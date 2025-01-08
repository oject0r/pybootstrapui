from .base import HTMLElement
from pybootstrapui.components.dynamics.queue import add_task


class File:
	"""
    Represents a file object with metadata.

    Attributes:
        name (str): The name of the file.
        path (str): The path of the file.
        size (int): The size of the file in bytes.
        type (str): The MIME type of the file.
    """

	def __init__(self, name: str, size: int, type: str, path: str = ""):
		"""
        Initializes a File object.

        Args:
            name (str): The name of the file.
            size (int): The size of the file in bytes.
            type (str): The MIME type of the file.
            path (str): The path of the file (default is an empty string).
        """
		self.name = name
		self.path = path
		self.size = size
		self.type = type


class FileUpload(HTMLElement):
	"""
    A class representing a file upload input component.

    Attributes:
        accept (str): Accepted file types (e.g., "image/*", ".txt"). Defaults to '*'.
        multiple (bool): Whether to allow multiple file uploads. Defaults to False.
        label (str | None): Optional label for the file upload input.
        show_uploaded (bool): Whether to display the uploaded files in a list. Defaults to True.
        classes (list[str] | None): Additional CSS classes for customization.
    """

	def __init__(
			self,
			accept: str = "*",
			multiple: bool = False,
			label: str | None = None,
			show_uploaded: bool = True,
			classes: list[str] | None = None,
			id: str | None = None,
	):
		"""
        Initializes a file upload input.

        Args:
            accept (str): Accepted file types (default is '*').
            multiple (bool): Whether multiple files can be selected (default is False).
            label (str | None): Optional label for the input.
            show_uploaded (bool): Whether to display uploaded files in a list (default is True).
            classes (list[str] | None): Additional CSS classes.
            id (str | None): Unique identifier for the input.
        """
		super().__init__(classes, id)
		self.accept = accept
		self.multiple = multiple
		self.label = label
		self.show_uploaded = show_uploaded

	def construct(self) -> str:
		"""
        Constructs the HTML and JavaScript representation of the file upload component.

        Returns:
            str: Combined HTML and JavaScript as a string.
        """
		multiple_attr = "multiple" if self.multiple else ""
		return f"""
        <div class="file-upload-container">
            <button class="file-upload-button" id="{self.id}-browse-files">
                <i class="bi bi-folder-plus"></i> {self.label or "Browse Files"}
            </button>
            <ul id="{self.id}-uploaded-files" class="uploaded-files"></ul>
            <input type="file" id="{self.id}" class="file-upload-input" style="display: none;" {multiple_attr} accept="{self.accept}">
        </div>
        <script>
            (function() {{
                const fileInput = document.getElementById('{self.id}');
                const uploadedFiles = document.getElementById('{self.id}-uploaded-files');
                const browseButton = document.getElementById('{self.id}-browse-files');

                browseButton.addEventListener('click', () => {{
                    fileInput.value = '';
                    fileInput.click();
                }});

                fileInput.addEventListener('change', (event) => {{
                    handleFiles(event.target.files, '{self.id}');
                }});

                function handleFiles(files, inputId) {{
                    const inputElement = document.getElementById(inputId);
                    const uploadedFiles = document.getElementById(`${{inputId}}-uploaded-files`);

                    uploadedFiles.innerHTML = '';

                    {f'''
                    Array.from(files).forEach((file, index) => {{
                        const fileSize = (file.size / 1024 / 1024).toFixed(2) + ' MB';

                        const listItem = document.createElement('li');
                        listItem.innerHTML = 
                            `<span class="file-name"><i class="bi bi-file-earmark"></i> ${{file.name}}</span>
                            <span class="file-size">${{fileSize}}</span>
                            <span class="delete-button" onclick="deleteFile('${{inputId}}', ${{index}}, this.parentElement)">
                                <i class="bi bi-trash"></i>
                            </span>`;
                        uploadedFiles.appendChild(listItem);
                    }});
                    ''' if self.show_uploaded else ''}
                }}

                function deleteFile(inputId, index, listItem) {{
                    const inputElement = document.getElementById(inputId);

                    if (!inputElement || !inputElement.files) {{
                        console.error('File input not found or unsupported.');
                        return;
                    }}

                    const dataTransfer = new DataTransfer();
                    const files = Array.from(inputElement.files);

                    files.forEach((file, i) => {{
                        if (i !== index) {{
                            dataTransfer.items.add(file);
                        }}
                    }});

                    inputElement.files = dataTransfer.files;
                    listItem.remove();

                    if (dataTransfer.files.length === 0) {{
                        inputElement.value = '';
                    }}
                }}
            }})();
        </script>
        """

	async def get_files(self) -> list[File]:
		"""
        Queues a task to get the list of selected files dynamically.

        Returns:
            list[File]: A list of selected files with their metadata.

        Example:
            files = await file_upload.get_files()
            for file in files:
                print(file.name, file.size, file.type, file.path)
        """
		task = add_task(self.id, "getSelectedFiles")
		await task.wait_async()

		return [
			File(
				result["name"], result["size"], result["type"], result.get("path", "")
			)
			for result in task.result.get()
		]
