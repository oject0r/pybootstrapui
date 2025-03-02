from typing import Callable, Awaitable

import pybootstrapui.components.dynamics.queue as queue
import uuid


class HTMLElement:
    """A class representing a basic HTML element."""

    def __init__(self, classes: list[str] | None = None, unique_id: str | None = None):
        """Initializes an HTMLElement object.

        Args:
            classes (list[str] | None): A list of CSS classes to apply to the element.
            unique_id (str | None): A unique identifier for the element.

        Notes:
            If `unique_id` is not provided, a random UUID will be used.
        """
        self.classes = classes or []
        self.classes_str = " ".join(self.classes).strip(" ")
        self.id = unique_id or f"PyBootstrapUIElement_{uuid.uuid4().hex}"
        self.special_id = hash(self) * 400

    def add_class(self, *classnames: str):
        """Adds one or more classes to the element and updates the class string."""
        self.classes.extend(classnames)
        self.classes_str = " ".join(self.classes).strip(" ")

    def remove_class(self, classname: str):
        """Removes a class from the element and updates the class string."""
        if classname in self.classes:
            self.classes.remove(classname)
            self.classes_str = " ".join(self.classes).strip(" ")

    def construct(self) -> str:
        """Converts the object into an HTML string."""
        raise NotImplementedError(
            "The `construct` method must be implemented by subclasses."
        )

    def update(self, transition_time: int = 0) -> None:
        """Updates the HTML content of the element on the frontend by queuing a task.

        Replaces the current content of the element with the newly constructed HTML.
        """
        queue.add_task(
            self.id,
            "rewriteContent",
            newContent=self.construct(),
            transitionTime=transition_time,
        )

    def disable(self) -> None:
        """Disables the element."""
        queue.add_task(self.id, "disableElement")

    def enable(self) -> None:
        """Enables the element."""
        queue.add_task(self.id, "enableElement")

    def remove(self) -> None:
        """Removes the element.

        This method deletes the current object.
        """
        queue.add_task(self.id, "deleteElement")
        del self

    def __repr__(self):
        return self.construct()


class RGBAColor:
    def __init__(self, red: int, green: int, blue: int, alpha: float = 1):
        """Init function."""
        self.r = red
        self.g = green
        self.b = blue
        self.a = alpha

    def construct(self):
        """Construct function."""
        return f'rgb({self.r} {self.g} {self.b} / {self.a})'


class HasValue(HTMLElement):
    value: any

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

        result = task.result.get()
        self.value = result

        return result

    def change_value(self, new_value: any):
        """
        Dynamically updates the value of the input element on the frontend.

        Args:
            new_value (str): The new value to be set in the input element.
        """
        queue.add_task(self.id, "setValue", value=new_value)
        self.value = new_value

    set_value = change_value


class Div(HTMLElement):
    """A class representing a <div> HTML element,
    which can contain child elements.
    """

    def __init__(
        self,
        *child_elements: HTMLElement,
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """Initializes a Div object."""
        super().__init__(classes, unique_id)
        self.child = child_elements

    def construct(self):
        """Converts the Div object into an HTML
        <div> element, including its child
        elements.
        """
        compiled_child = "\n".join([child.construct() for child in self.child])
        return f'<div id="{self.id}" class="{self.classes_str}">{compiled_child}</div>'
