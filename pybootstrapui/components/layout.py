from .base import HTMLElement
from typing_extensions import deprecated


@deprecated('Use Spacer instead (supports flex and margins)')
class Br(HTMLElement):  # Deprecated
	"""
	A class representing a <br> HTML element (line break).

	This class is deprecated and will be replaced by the Spacer class which supports more flexibility
	for layout, including margins and flex properties.
	"""

	def __init__(self):
		"""
		Initializes the Br object, which represents a <br> HTML element (line break).
		"""
		super().__init__()

	def construct(self) -> str:
		"""
		Converts the Br object into an HTML <br> element.

		Returns:
			- `str`: The HTML code for the <br> element.
		"""
		return '<br>'


class Hr(HTMLElement):
	"""
	A class representing an <hr> HTML element (horizontal line).
	"""

	def __init__(self):
		"""
		Initializes the Hr object, which represents an <hr> HTML element.
		"""
		super().__init__()

	def construct(self) -> str:
		"""
		Converts the Hr object into an HTML <hr> element.

		Returns:
			- `str`: The HTML code for the <hr> element.
		"""
		return '<hr>'


class Spacer(HTMLElement):
	"""
	A class representing a flexible spacer <div> element that supports customizable margins.

	This class is used to create spacing in layouts with support for top and bottom margins.
	"""

	def __init__(self, margin_top: str = '1em', margin_bottom: str = '1em'):
		"""
		Initializes the Spacer object with custom top and bottom margins.

		Parameters:
			- `margin_top` (str): The margin-top value (default is '1em').
			- `margin_bottom` (str): The margin-bottom value (default is '1em').
		"""
		self.mt = margin_top
		self.mb = margin_bottom
		super().__init__()

	def construct(self) -> str:
		"""
		Converts the Spacer object into an HTML <div> element with customizable margins.

		Returns:
			- `str`: The HTML code for the <div> element that acts as a spacer.
		"""
		return f'<div style="width: 100%; margin-top: {self.mt}; margin-bottom: {self.mb}"></div>'
