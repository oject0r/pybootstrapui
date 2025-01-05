import pybootstrapui.components.dynamics.queue as queue
import uuid


class HTMLElement:
    """A class representing a basic HTML element.

    :var - classes: A list of CSS classes for the element.
    :type - classes: list[str] | None
    :var - unique_id: A unique identifier for the element.
    :type - unique_id: str | None
    :var - classes_str: A string representation of the classes, joined by spaces.
    :type - classes_str: str
    :var - id: A unique identifier for the element.
    :type - id: str | None
    """

    def __init__(self, classes: list[str] | None = None, unique_id: str | None = None):
        """Initializes an HTMLElement object.

        Parameters:
                - classes (list[str] | None): A list of CSS classes for the element (default is None).
                - unique_id (str | None): A unique identifier for the element (default is None).
        """
        self.classes = classes or []
        self.classes_str = " ".join(self.classes).strip(" ")
        self.id = unique_id or f"PyBootstrapUIElement_{uuid.uuid4().hex}"
        self.special_id = hash(self) * 400

    def add_class(self, classname: str):
        """Adds a class to the element and
        updates the class string.

        Parameters:
                - classname (str): The class name to add.
        """
        self.classes.append(classname)
        self.classes_str = " ".join(self.classes).strip(" ")

    def remove_class(self, classname: str):
        """Removes a class from the element and
        updates the class string.

        Parameters:
                - classname (str): The class name to remove.
        """
        if classname in self.classes:
            self.classes.remove(classname)
            self.classes_str = " ".join(self.classes).strip(" ")

    def construct(self) -> str:
        """Converts the object into an HTML
        string.

        Not implemented in the base class.
        :return: An empty string in the base class.
        :rtype: - str
        """
        return ""

    def update(self, transition_time=0) -> None:
        """Updates the HTML content of the
        element on the frontend by queuing a
        task.

        Replaces the current content of the
        element with the newly constructed HTML.
        """
        queue.add_task(
            self.id,
            "rewriteContent",
            newContent=self.construct(),
            transitionTime=transition_time,
        )

    def remove(self):
        """Removes the element.

        This method deletes the current object.
        """
        queue.add_task(self.id, "deleteElement")
        del self


class RGBAColor:
    def __init__(self, red: int, green: int, blue: int, alpha: float = 0):
        """Init function."""
        self.r = red
        self.g = green
        self.b = blue
        self.a = alpha

    def construct(self):
        """Construct function."""
        return f'rgba({self.r}, {self.g}, {self.b}, {self.a})'


class Div(HTMLElement):
    """A class representing a <div> HTML element,
    which can contain child elements.

    :var - child: A list of child HTMLElement objects to be included inside the <div>.
    :type - child: list[HTMLElement]
    """

    def __init__(
        self,
        child_elements: list[HTMLElement],
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """Initializes a Div object.

        Parameters:
                - child_elements (list[HTMLElement]): A list of child elements to include inside the <div>.
                - classes (list[str] | None): A list of CSS classes for the <div> (default is None).
                - unique_id (str | None): A unique identifier for the <div> (default is None).
        """
        super().__init__(classes, unique_id)
        self.child = child_elements

    def construct(self):
        """Converts the Div object into an HTML
        <div> element, including its child
        elements.

        :return: The HTML code for the <div> element with its child elements.
        :rtype: - str
        """
        compiled_child = "\n".join([child.construct() for child in self.child])
        return f'<div id="{self.id}" class="{self.classes_str}">{compiled_child}</div>'
