import random
from typing import Callable, Awaitable, Union
from .base import HTMLElement
from pybootstrapui.components.dynamics.client_to_server import add_handler
from pybootstrapui.utils.callbacks import wrap_callback


class Button(HTMLElement):
	"""
	A class representing a <button> HTML element.

	Attributes:
		- `label` (str): The text label of the button.
		- `on_click` (str | None): The JavaScript function to call when the button is clicked (default is None).
		- `style_type` (str): The style type of the button (default is 'primary').
		- `type` (str | None): The type of the button (e.g., 'submit', 'button', etc.).
		- `callback` (Callable | None): A server-side function to handle button clicks (default is None).
	"""

	def __init__(self, label: str, on_click: str | None = None, btn_type: str | None = None,
				 btn_style_type: str = 'primary', classes: list[str] | None = None, unique_id: str | None = None,
				 callback: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None):
		"""
		Initializes a Button object.

		Parameters:
			- `label` (str): The text label of the button.
			- `on_click` (str | None): The JavaScript function to call when the button is clicked (default is None).
			- `btn_type` (str | None): The type of the button (e.g., 'submit', 'button', etc., default is None).
			- `btn_style_type` (str): The style type of the button (default is 'primary').
			- `classes` (list[str] | None): A list of CSS classes for the button (default is None).
			- `unique_id` (str | None): A unique identifier for the button (default is None).
			- `callback` (Callable | Awaitable | None): A server-side function to handle button clicks (default is None).

		Note:
			- If no `unique_id` is provided, an ID is automatically generated.
			- If a callback is provided, it is automatically registered with the server.
		"""
		super().__init__(classes, unique_id)
		self.label = label
		self.on_click = on_click
		self.style_type = btn_style_type
		self.type = btn_type
		self.callback = callback or None

		# Register the callback if provided
		if callback and self.id:
			add_handler('button_click', self.id, wrap_callback(callback))

	def register_callback(self, on_click: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None):
		"""
		Registers a callback for the button click event.

		Parameters:
			- `on_click` (Callable | Awaitable | None): The callback function to execute when the button is clicked.

		Notes:
			- If a callback is already registered, it will not be replaced.
		"""
		if not self.callback:
			self.callback = on_click
			add_handler('button_click', self.id, wrap_callback(self.callback))

	def construct(self):
		"""
		Converts the Button object into an HTML <button> element.

		Returns:
			- `str`: The HTML code for the <button> element.
		"""
		# Prepare optional attributes
		type_attr = f'type="{self.type}"' if self.type else ''
		id_attr = f'id="{self.id}"' if self.id else ''
		onclick_attr = f'onclick="{self.on_click}"' if self.on_click else f'onclick="sendButtonClick(\'{self.id}\')"'

		# Generate the HTML string
		return f'''
			<button {type_attr} class="btn btn-{self.style_type} {self.classes_str}" {id_attr} {onclick_attr}>
				{self.label}
			</button>
		'''


class ButtonGroup(HTMLElement):
	"""
	A class representing a group of <button> HTML elements, wrapped in a <div> element.

	Attributes:
		- `buttons` (list[Button]): A list of Button objects to be grouped together.
	"""

	def __init__(self, buttons: list[Button], classes: list[str] | None = None, unique_id: str | None = None):
		"""
		Initializes a ButtonGroup object.

		Parameters:
			- `buttons` (list[Button]): A list of Button objects to be grouped together.
			- `classes` (list[str] | None): A list of CSS classes for the button group (default is None).
			- `unique_id` (str | None): A unique identifier for the button group (default is None).
		"""
		super().__init__(classes, unique_id)
		self.buttons = buttons

	def construct(self):
		"""
		Converts the ButtonGroup object into an HTML <div> containing all the buttons.

		Returns:
			- `str`: The HTML code for the <div> element containing all the buttons in the group.
		"""
		buttons_compiled = '\n'.join([button.construct() for button in self.buttons])
		return f'''
		<div class="btn-group" id="{self.id if self.id else ''}" class="{self.classes_str}">
			{buttons_compiled}
		</div>
		'''
