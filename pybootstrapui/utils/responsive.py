class ResponsiveUtilities:
    """A utility class for managing Bootstrap
    responsive utilities, including visibility
    and spacing."""

    def __init__(self):
        self.classes = []

    def add_visibility_class(self, size: str, display: str):
        """Adds a visibility control class based
        on the screen size and display type.

        Parameters:
            size (str): Screen size (e.g., sm, md, lg, etc.).
            display (str): Display type (e.g., none, block, inline, etc.).
        """
        self.classes.append(f"d-{size}-{display}")

    def add_spacing_class(self, property: str, size: str, value: int):
        """Adds a spacing class based on the
        property, screen size, and value.

        Parameters:
            property (str): Spacing property (e.g., m, p, mt, mb).
            size (str): Screen size (e.g., sm, md, lg, etc.).
            value (int): Spacing value (0 to 5).
        """
        self.classes.append(f"{property}-{size}-{value}")

    def construct(self) -> str:
        """Returns the full class string for the
        responsive utilities.
        """
        return " ".join(self.classes)
