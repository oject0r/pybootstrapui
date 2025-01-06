from .base import HTMLElement


class GridSystem:
    """
    A class representing a Bootstrap grid system.

    This class provides a way to construct a grid layout using Bootstrap's row and column structure.

    Attributes:
        elements (list[HTMLElement]): List of elements inside the grid container.
        row (bool): Indicates whether this is a row container. Defaults to True.
        cols (str): Grid column classes (e.g., "col-md-6 col-lg-4"). Defaults to an empty string.
        classes (list[str]): Additional custom classes for the grid container.
    """

    def __init__(
        self,
        *elements: HTMLElement,
        row: bool = True,
        cols: str = "",
        classes: list[str] = None,
    ):
        """
        Initializes the GridSystem object.

        Args:
            elements (list[HTMLElement] | None): List of elements inside the grid container. Defaults to None.
            row (bool): Indicates whether this is a row container. Defaults to True.
            cols (str): Grid column classes. Defaults to an empty string.
            classes (list[str] | None): Additional custom classes for the grid container. Defaults to None.

        Example:
            # Create a grid system with multiple elements
            grid = GridSystem(
                elements=[Div(classes=["col-md-6"]), Div(classes=["col-md-6"])],
                row=True,
                classes=["custom-grid"]
            )
        """
        self.elements = elements if elements else []
        self.row = row
        self.cols = cols
        self.classes = classes if classes else []

    def add_element(self, element: HTMLElement):
        """
        Adds an element to the grid.

        Args:
            element (HTMLElement): The HTML element to add to the grid.

        Example:
            # Add a new element to the grid
            grid.add_element(Div(classes=["col-md-4"]))
        """
        self.elements.append(element)

    def construct(self) -> str:
        """
        Constructs the HTML string for the grid container.

        Returns:
            str: The HTML string representing the grid system.

        Example:
            # Render the grid system as HTML
            html = grid.construct()
        """
        container_class = "row" if self.row else "col"
        if self.cols:
            container_class += f" {self.cols}"
        additional_classes = " ".join(self.classes)
        child_html = "\n".join([element.construct() for element in self.elements])
        return f'<div class="{container_class} {additional_classes}">{child_html}</div>'
