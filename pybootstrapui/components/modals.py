from .base import HTMLElement


class Modal(HTMLElement):
	"""
	A class for creating Bootstrap modals.

	Attributes:
		- `title` (str | None): The modal's title.
		- `body` (list[HTMLElement]): Child elements within the modal body.
		- `footer` (list[HTMLElement]): Child elements within the modal footer.
		- `classes` (list[str] | None): Additional CSS classes for the modal.
		- `unique_id` (str | None): Unique identifier for the modal.
	"""

	def __init__(self, title: str | None = None, body: list[HTMLElement] | None = None,
				 footer: list[HTMLElement] | None = None,
				 classes: list[str] | None = None, unique_id: str | None = None):
		"""
		Initializes the Modal object with title, body, footer, and optional CSS classes.

		Parameters:
			- `title` (str | None): The modal's title (optional).
			- `body` (list[HTMLElement] | None): Child elements for the modal body (default: empty list).
			- `footer` (list[HTMLElement] | None): Child elements for the modal footer (default: empty list).
			- `classes` (list[str] | None): Additional CSS classes for the modal (optional).
			- `unique_id` (str | None): Unique identifier for the modal (optional).

		Example:
			```
			modal = Modal(
				title="My Modal",
				body=[TextElement("This is the modal body.")],
				footer=[Button("Close", classes=["btn", "btn-secondary"])]
			)
			```
		"""
		super().__init__(classes, unique_id)
		self.title = title
		self.body = body if body else []
		self.footer = footer if footer else []

	def add_body_element(self, element: HTMLElement):
		"""
		Adds a child element to the modal body.

		Parameters:
			- `element` (HTMLElement): The element to add.

		Example:
			```
			modal.add_body_element(TextElement("New body content"))
			```
		"""
		self.body.append(element)

	def add_footer_element(self, element: HTMLElement):
		"""
		Adds a child element to the modal footer.

		Parameters:
			- `element` (HTMLElement): The element to add.

		Example:
			```
			modal.add_footer_element(Button("Save Changes"))
			```
		"""
		self.footer.append(element)

	def construct(self) -> str:
		"""
		Constructs the HTML for the modal.

		Returns:
			- `str`: The HTML representation of the modal.

		Example:
			```
			html = modal.construct()
			print(html)
			```
		"""
		header_html = f'''
		<div class="modal-header">
			<h5 class="modal-title">{self.title}</h5>
			<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
		</div>
		''' if self.title else ""

		body_html = "\n".join([child.construct() for child in self.body])
		footer_html = "\n".join([child.construct() for child in self.footer])
		classes_str = " ".join((self.classes or []) + ["modal", "fade"])
		id_attr = f'id="{self.id}"' if self.id else ''

		return f'''
		<div class="{classes_str}" {id_attr} tabindex="-1">
			<div class="modal-dialog">
				<div class="modal-content">
					{header_html}
					<div class="modal-body">{body_html}</div>
					<div class="modal-footer">{footer_html}</div>
				</div>
			</div>
		</div>
		'''
