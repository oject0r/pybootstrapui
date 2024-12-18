from .base import HTMLElement


class BootstrapIcon(HTMLElement):
	"""
	A class representing a Bootstrap icon.

	This class generates an HTML <i> element with the specified Bootstrap icon class.

	Attributes:
		icon (str): The name of the Bootstrap icon.
	"""

	def __init__(self, icon_name: str):
		"""
		Initializes a BootstrapIcon object with the specified icon name.

		Parameters:
			icon_name (str): The name of the Bootstrap icon.
		"""
		super().__init__()
		self.icon = icon_name

	def construct(self):
		"""
		Generates the HTML code for the Bootstrap icon.

		Returns:
			str: The HTML code for the <i> element with the Bootstrap icon class.
		"""
		return f'<i class="bi bi-{self.icon}"></i>'


class TextObject(HTMLElement):
	"""
	A class representing a text element in HTML, with customizable properties such as font size, text type, and classes.

	This class generates HTML tags like <p>, <h1>, <a>, etc., with options for font size, classes, unique IDs, and hyperlinks.

	Attributes:
		label (str): The text content to display.
		size (int): The font size for the text (default is 18).
		id (str | None): The unique ID for the text element (optional).
		type (str): The type of HTML tag to use (default is 'p').
		href (str | None): The hyperlink target (only relevant if the text is a link).
	"""

	def __init__(self, label: str, font_size: int = 18, classes: list[str] | None = None,
				 unique_id: str | None = None, text_type: str = 'p', href: str | None = None):
		"""
		Initializes a TextObject with the specified properties.

		Parameters:
			label (str): The text content to display.
			font_size (int): The font size for the text (default is 18).
			classes (list[str] | None): Optional list of classes to apply to the element.
			unique_id (str | None): Optional unique ID for the element.
			text_type (str): The type of HTML tag to use (default is 'p').
			href (str | None): The URL for the hyperlink (relevant only for 'a' type).
		"""
		super().__init__(classes, unique_id)
		self.label = label
		self.size = font_size
		self.type = text_type
		self.href = href

	def construct(self):
		"""
		Generates the HTML code for the text element.

		Returns:
			str: The HTML code for the text element with the specified properties.
		"""
		self.label = self.label.replace('\n', '<br>')
		return f"""
		<{self.type} {'href="{href}"'.format(href=self.href) if self.href else ''} 
		{'class="{classes}"'.format(classes=self.classes_str)} 
		{'id="{id}"'.format(id=self.id) if self.id else ''} 
		{'style="font-size: {size}px;"'.format(size=self.size) if self.size else ''}>
		{self.label}</{self.type}>
		"""


def bold(text: any, classes: list[str] | str = ''):
	"""
	Creates a bold HTML element.

	Parameters:
		text (any): The text or content to be bolded.
		classes (list[str] | str): Optional list of classes to apply to the <b> element.

		Returns:
			str: The HTML code for a <b> element containing the bolded text.
	"""
	text = str(text)
	if type(classes) == list:
		classes = ' '.join(classes)
	return f'<b class="{classes}">{text}</b>'


def italic(text: str):
	"""
	Creates an italic HTML element.

	Parameters:
		text (str): The text to be italicized.

		Returns:
			str: The HTML code for an <i> element containing the italicized text.
	"""
	text = str(text)
	return f'<i>{text}</i>'


class Text(TextObject):
	"""
	A class representing a standard text element (<p>) with a default font size of 24px.

	Inherits from TextObject and applies a default font size.

	Attributes:
		label (str): The text content to display.
		classes (list[str] | None): Optional list of classes to apply to the element.
		unique_id (str | None): Optional unique ID for the element.
	"""

	def __init__(self, label: str, font_size: int = 18, classes: list[str] | None = None, unique_id: str | None = None):
		"""
		Initializes a Text object.

		Parameters:
			label (str): The text content to display.
			classes (list[str] | None): Optional list of classes to apply to the element.
			unique_id (str | None): Optional unique ID for the element.
		"""
		super().__init__(label, font_size, classes, unique_id)


class Link(TextObject):
	"""
	A class representing a hyperlink (<a>) element with customizable text content, font size, and target URL.

	Inherits from TextObject and sets the text type to 'a' for anchor links.

	Attributes:
		label (str): The text content to display for the link.
		href (str): The target URL for the link.
		classes (list[str] | None): Optional list of classes to apply to the element.
		unique_id (str | None): Optional unique ID for the element.
	"""

	def __init__(self, label: str, href: str, font_size: int = 18, classes: list[str] | None = None,
				 unique_id: str | None = None):
		"""
		Initializes a Link object with the specified label, href, and optional styling.

		Parameters:
			label (str): The text content to display for the link.
			href (str): The target URL for the link.
			font_size (int): The font size for the link (default is 18).
			classes (list[str] | None): Optional list of classes to apply to the <a> element.
			unique_id (str | None): Optional unique ID for the <a> element.
		"""
		super().__init__(label, font_size, classes, unique_id, 'a', href)


class Header(TextObject):
	"""
	A class representing a header element (h1, h2, etc.) with an optional Bootstrap icon.

	Inherits from TextObject and allows for the creation of headers with customizable size (1-6), icon, and other properties.

	Attributes:
		label (str): The text content for the header.
		header_size (int): The size of the header (1-6). Defaults to 1 (h1).
		bootstrap_icon (BootstrapIcon | None): An optional Bootstrap icon to display in the header.
		classes (list[str] | None): Optional list of classes to apply to the header element.
		unique_id (str | None): Optional unique ID for the header element.
	"""

	def __init__(self, label: str, header_size: int = 1, bi: BootstrapIcon | None = None,
				 classes: list[str] | None = None, unique_id: str | None = None):
		"""
		Initializes a Header object with the specified properties.

		Parameters:
			label (str): The text content for the header.
			header_size (int): The size of the header (1-6), default is 1.
			bi (BootstrapIcon | None): An optional Bootstrap icon to display in the header.
			classes (list[str] | None): Optional list of classes to apply to the header element.
			unique_id (str | None): Optional unique ID for the header element.
		"""
		super().__init__(label, 64, classes, unique_id)
		self.bootstrap_icon = bi
		self.header_size = header_size
		self.label = label

	def construct(self):
		"""
		Generates the HTML for the header element with the specified properties.

		Returns:
			str: The HTML code for the header with the optional icon and label.

		Raises:
			ValueError: If the header size is not between 1 and 6.
		"""
		self.label = self.label.replace('\n', '<br>')
		if self.header_size > 6 or self.header_size < 1:
			raise ValueError('Header size must be from 1 to 6!')
		return f"""
		<h{self.header_size} {'class="{classes}"'.format(classes=self.classes_str)} 
		{'id="{id}"'.format(id=self.id) if self.id else ''}>
		{self.bootstrap_icon.construct() if self.bootstrap_icon else ''} 
		{self.label}</h{self.header_size}>
		"""
