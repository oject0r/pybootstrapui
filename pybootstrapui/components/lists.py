from .base import HTMLElement


class ListElement(HTMLElement):
	"""
	A class representing an individual list item (<li>) element that can contain other elements.

	Attributes:
		- `child` (list[HTMLElement]): A list of child elements to include inside the <li>.
		- `classes` (list[str] | None): Optional list of classes to apply to the <li> element.
		- `unique_id` (str | None): Optional unique ID for the <li> element.
	"""

	def __init__(self, child_elements: list[HTMLElement], classes: list[str] | None = None,
				 unique_id: str | None = None):
		"""
		Initializes a ListElement with the specified child elements, classes, and unique ID.

		Parameters:
			- `child_elements` (list[HTMLElement]): The child elements to be included inside the <li>.
			- `classes` (list[str] | None): Optional list of classes to apply to the <li> element.
			- `unique_id` (str | None): Optional unique ID for the <li> element.
		"""
		super().__init__(classes, unique_id)
		self.child = child_elements

	def construct(self) -> str:
		"""
		Generates the HTML for the <li> element, including its child elements.

		Returns:
			- `str`: The HTML code for the <li> element with its children.
		"""
		compiled_child = '\n'.join([child.construct() for child in self.child])
		id_attr = f'id="{self.id}"' if self.id else ''
		return f'<li class="{self.classes_str}" {id_attr}>{compiled_child}</li>'


class List(HTMLElement):
	"""
	A class representing an unordered list (<ul>) element containing multiple ListElements.

	Attributes:
		- `child` (list[ListElement]): A list of ListElement objects to be included inside the <ul>.
		- `classes` (list[str] | None): Optional list of classes to apply to the <ul> element.
		- `unique_id` (str | None): Optional unique ID for the <ul> element.
	"""

	def __init__(self, elements: list[ListElement], classes: list[str] | None = None, unique_id: str | None = None):
		"""
		Initializes a List object with the specified ListElements, classes, and unique ID.

		Parameters:
			- `elements` (list[ListElement]): The ListElement objects to include in the list.
			- `classes` (list[str] | None): Optional list of classes to apply to the <ul> element.
			- `unique_id` (str | None): Optional unique ID for the <ul> element.
		"""
		super().__init__(classes, unique_id)
		self.child = elements

	def construct(self) -> str:
		"""
		Generates the HTML for the <ul> element, including all ListElement children.

		Returns:
			- `str`: The HTML code for the <ul> element with its ListElement children.
		"""
		compiled_child = '\n'.join([child.construct() for child in self.child])
		id_attr = f'id="{self.id}"' if self.id else ''
		return f'<ul class="{self.classes_str}" {id_attr}>{compiled_child}</ul>'
