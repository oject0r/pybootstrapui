import random
from . import add_handler
from .base import HTMLElement
from typing import Literal, Callable, Union, Awaitable
import pybootstrapui.components.dynamics.queue as queue
from pybootstrapui.utils.callbacks import wrap_callback


class InputObject(HTMLElement):
    """
    Represents an input element with customizable properties and event handlers.

    Attributes:
        label (str | None): Optional label for the input element.
        type (Literal): The type of the input (e.g., text, email, password, etc.).
        placeholder (str | None): Placeholder text for the input.
        prefix (str | None): Optional text displayed as a prefix.
        classes (list[str] | None): CSS classes to apply to the input element.
        id (str | None): Unique identifier for the input element.
        name (str | None): Name attribute for the input.
        value (str | None): Default value for the input field.
        required (bool): Whether the input field is required.
        tag (str): The tag type (default is 'input', can be 'textarea').
        on_input (Callable | Awaitable | None): Callback for handling the input event.
        on_focus (Callable | Awaitable | None): Callback for handling the focus event.
        on_blur (Callable | Awaitable | None): Callback for handling the blur event.
    """

    def __init__(
        self,
        label: str,
        input_type: Literal[
            "button",
            "checkbox",
            "color",
            "date",
            "datetime-local",
            "email",
            "file",
            "hidden",
            "image",
            "month",
            "password",
            "radio",
            "range",
            "reset",
            "search",
            "submit",
            "tel",
            "text",
            "time",
            "url",
            "week",
            "number",
        ] = "text",
        *,
        placeholder: str | None = None,
        prefix_text: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
        name: str | None = None,
        value: str | None = None,
        required: bool = False,
        tag_type: str = "input",
        on_input: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
        on_focus: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
        on_blur: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
    ):
        """
        Initializes an InputObject with customizable properties.

        Args:
            label (str): The label text for the input element.
            input_type (Literal): The type of the input element (e.g., text, email).
            placeholder (str | None): Placeholder text for the input field.
            prefix_text (str | None): Optional prefix displayed before the input.
            classes (list[str] | None): CSS classes for the input element.
            id (str | None): Unique identifier for the input element.
            name (str | None): The name attribute for the input.
            value (str | None): Default value for the input field.
            required (bool): Whether the input is required.
            tag_type (str): The HTML tag type (e.g., 'input', 'textarea').
            on_input (Callable | Awaitable | None): Callback for handling input events.
            on_focus (Callable | Awaitable | None): Callback for handling focus events.
            on_blur (Callable | Awaitable | None): Callback for handling blur events.
        """
        super().__init__(classes, id)

        self.label = label
        self.type = input_type
        self.prefix = prefix_text or ""
        self.placeholder = placeholder or ""
        self.name = name or ""
        self.value = value or ""
        self.required = required
        self.tag = tag_type
        self.on_input = on_input
        self.on_focus = on_focus
        self.on_blur = on_blur

        if not self.id:
            self.id = f"i{self.special_id * 3919 * random.randint(3, 5)}"

        self.register_callbacks(
            on_input=self.on_input, on_focus=self.on_focus, on_blur=self.on_blur
        )

    def register_callbacks(
        self,
        *,
        on_input: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
        on_focus: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
        on_blur: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
    ):
        """
        Registers or updates callbacks for events like `on_input`, `on_focus`, and `on_blur`.

        Args:
            on_input (Callable | Awaitable | None): Callback for handling the input event.
            on_focus (Callable | Awaitable | None): Callback for handling the focus event.
            on_blur (Callable | Awaitable | None): Callback for handling the blur event.

        Note:
            If a handler is already registered, it will be replaced.
        """
        if on_input:
            self.on_input = on_input
            add_handler("on_input", self.id, wrap_callback(on_input))

        if on_focus:
            self.on_focus = on_focus
            add_handler("on_focus", self.id, wrap_callback(on_focus))

        if on_blur:
            self.on_blur = on_blur
            add_handler("on_blur", self.id, wrap_callback(on_blur))

    def update_value(self, value: str | None):
        """
        Updates the value of the input field locally before rendering.

        Args:
            value (str | None): The new value for the input field. If None, resets to an empty string.
        """
        self.value = value or ""

    async def get_value(self) -> any:
        """
        Asynchronously retrieves the value of an input element from the frontend.

        Returns:
            any: The value of the input element, as returned by the frontend.
            None: If the element does not have an `id`.

        Example:
            value = await input_element.get_value()
            print(f"The input value is: {value}")
        """
        if not self.id:
            return

        task = queue.add_task(self.id, "getValue")
        await task.wait_async()
        return task.result.get()

    def change_value(self, new_value: str):
        """
        Dynamically updates the value of the input element on the frontend.

        Args:
            new_value (str): The new value to be set in the input element.
        """
        queue.add_task(self.id, "setValue", value=new_value)
        self.value = new_value

    def construct(self) -> str:
        """
        Generates the HTML for the input element.

        Returns:
            str: The HTML code for the input element.
        """
        return f"""
        <div class="input-group mb-3">
            {f'<span class="input-group-text">{self.prefix}</span>' if self.prefix else ''}
            <div class="form-floating {self.classes_str}">
                <{self.tag} class="form-control"
                    id="{self.id}" type="{self.type}" name="{self.name}" value="{self.value}"
                    placeholder="{self.placeholder}" {'required' if self.required else ''}
                >
                </{self.tag}>
                <label for="{self.id}">{self.label}</label>
            </div>
        </div>
        """


class TextInput(InputObject):
    """A class for a text input element."""

    def __init__(
        self,
        label: str,
        placeholder: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
        name: str | None = None,
        value: str | None = None,
        required: bool = False,
    ):
        super().__init__(
            label,
            input_type="text",
            placeholder=placeholder,
            classes=classes,
            id=id,
            name=name,
            value=value,
            required=required,
        )

class Input(TextInput):
    pass

class IntInput(InputObject):
    """A class for an integer input element."""

    def __init__(
        self,
        label: str,
        placeholder: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
        name: str | None = None,
        value: str | None = None,
        required: bool = False,
    ):
        super().__init__(
            label,
            input_type="number",
            placeholder=placeholder,
            classes=classes,
            id=id,
            name=name,
            value=value,
            required=required,
        )


class EmailInput(InputObject):
    """A class for an email input element."""

    def __init__(
        self,
        label: str,
        placeholder: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
        name: str | None = None,
        value: str | None = None,
        required: bool = False,
    ):
        super().__init__(
            label,
            input_type="email",
            placeholder=placeholder,
            classes=classes,
            id=id,
            name=name,
            value=value,
            required=required,
        )


class PasswordInput(InputObject):
    """A class for a password input element."""

    def __init__(
        self,
        label: str,
        placeholder: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
        name: str | None = None,
        value: str | None = None,
        required: bool = False,
    ):
        super().__init__(
            label,
            input_type="password",
            placeholder=placeholder,
            classes=classes,
            id=id,
            name=name,
            value=value,
            required=required,
        )


class TextArea(InputObject):
    """A class for a textarea input element."""

    def __init__(
        self,
        label: str,
        placeholder: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
        name: str | None = None,
        value: str | None = None,
        required: bool = False,
    ):
        super().__init__(
            label,
            input_type="text",
            placeholder=placeholder,
            classes=classes,
            id=id,
            name=name,
            value=value,
            required=required,
            tag_type="textarea",
        )
