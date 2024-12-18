from .base import HTMLElement
from .text import Header


class Card(HTMLElement):
	"""
	A class to generate a card component with optional header and child elements.

	Attributes:
		- `header` (Header | None): An optional header for the card.
		- `child` (list[HTMLElement]): A list of child elements to be included in the card body.
	"""

	def __init__(self, child_elements: list[HTMLElement], header: Header | None = None,
				 unique_id: str | None = None, classes: list[str] | None = None) -> None:
		"""
		Initializes the Card with optional header and child elements.

		Parameters:
			- `child_elements` (list[HTMLElement]): The child elements to be included inside the card.
			- `header` (Header | None): An optional header for the card.
			- `unique_id` (str | None): An optional unique ID for the card.
			- `classes` (list[str] | None): Optional list of CSS classes for styling the card.

		Example:
			# Create a card with a header and child elements
			```
			card = Card(
				child_elements=[paragraph, button],
				header=Header("Card Header"),
				classes=["custom-card"]
			)
			```

		Note:
			- The `classes` parameter allows adding custom CSS styles.
			- If `header` is provided, it will be rendered at the top of the card.
		"""
		super().__init__(classes, unique_id)
		self.header = header
		self.child = child_elements

	def construct(self):
		"""
		Generates the HTML code for the card, including its body and header (if provided).

		Returns:
			- `str`: The HTML code for the card element.

		Example:
			# Render the card into HTML
			```
			html = card.construct()
			```
		"""
		header_html = f'<div class="card-header">{self.header.construct()}</div>' if self.header else ''
		body_html = '\n'.join([child.construct() for child in self.child])

		return f'''
		<div class="card mb-4" id="{self.id}" class="{self.classes_str}">
			{header_html}
			<div class="card-body">
				{body_html}
			</div>
		</div>
		'''
