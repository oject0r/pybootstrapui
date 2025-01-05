import random
from typing import Callable, Awaitable, Union
from .base import HTMLElement
from pybootstrapui.components.dynamics.client_to_server import add_handler
from pybootstrapui.utils.callbacks import wrap_callback


class Button(HTMLElement):
    """
    A class representing a `<button>` HTML element.

    Attributes:
            - `label` (str): The text label of the button.
            - `style_type` (str): The style type of the button (default is 'primary').
            - `type` (str | None): The type of the button (e.g., 'submit', 'button', etc.).
            - `callback` (Callable | None): A server-side function to handle button clicks (default is None).
    """

    def __init__(
        self,
        label: str,
        on_click: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
        data: str | None = None,
        btn_type: str | None = None,
        btn_style_type: str = "primary",
        indicate_on_click_spinner: bool = True,
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """
        Initializes a Button object.

        Parameters:
                - `label` (str): The text label of the button.
                - `on_click` (Callable | Awaitable | None): A server-side function to handle button clicks (default is None).
                - `btn_type` (str | None): The type of the button (e.g., 'submit', 'button', etc., default is None).
                - `btn_style_type` (str): The style type of the button (default is 'primary').
                - `classes` (list[str] | None): A list of CSS classes for the button (default is None).
                - `unique_id` (str | None): A unique identifier for the button (default is None).

        Note:
                - If no `unique_id` is provided, an ID is automatically generated.
                - If a callback is provided, it is automatically registered with the server.
        """
        super().__init__(classes, unique_id)
        self.label = label
        self.style_type = btn_style_type
        self.type = btn_type
        self.callback = on_click or None
        self.indicate_callback = indicate_on_click_spinner
        data = data or ''
        self.data = data.replace('`', "'")

        # Register the callback if provided
        if on_click and self.id:
            add_handler("button_click", self.id, wrap_callback(on_click))

    def register_callback(
        self,
        on_click: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
    ):
        """
        Registers a callback for the button click event.

        Parameters:
                - `on_click` (Callable | Awaitable | None): The callback function to execute when the button is clicked.

        Notes:
                - If a callback is already registered, it will not be replaced.
        """
        if not self.callback:
            self.callback = on_click
            add_handler("button_click", self.id, wrap_callback(self.callback))

    def construct(self):
        """
        Converts the Button object into an HTML <button> element.

        Returns:
                - `str`: The HTML code for the <button> element.
        """
        # Prepare optional attributes
        type_attr = f'type="{self.type}"' if self.type else ""
        id_attr = f'id="{self.id}"' if self.id else ""
        onclick_attr = (
            f'onclick="sendButtonClick(\'{self.id}\', {"true" if self.indicate_callback else "false"}, `{self.data}`)"'
            if self.callback
            else ""
        )
        # Generate the HTML string
        return f"""
			<button {type_attr} class="btn btn-{self.style_type} {self.classes_str}" {id_attr} {onclick_attr}>
				{self.label}
			</button>
		"""


class ButtonGroup(HTMLElement):
    """
    A class representing a group of <button> HTML elements, wrapped in a <div> element.

    Attributes:
            - `buttons` (list[Button]): A list of Button objects to be grouped together.
    """

    def __init__(
        self,
        buttons: list[Button],
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
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
        buttons_compiled = "\n".join([button.construct() for button in self.buttons])
        return f"""
		<div class="btn-group {self.classes_str}" id="{self.id if self.id else ''}">
			{buttons_compiled}
		</div>
		"""
