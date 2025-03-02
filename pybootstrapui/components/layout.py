from .base import HTMLElement


class Br(HTMLElement):
    """
    Represents a <br> HTML element (line break).

    This class is deprecated and will be replaced by the `Spacer` class,
    which offers better flexibility for layout, including margin and flex properties.
    """

    def __init__(self):
        """
        Initializes a `Br` object representing an HTML <br> element.
        """
        super().__init__()

    def construct(self) -> str:
        """
        Converts the `Br` object into an HTML <br> element.

        Returns:
            str: The HTML string representing a <br> element.
        """
        return "<br>"

LineBreak = Br()

class Hr(HTMLElement):
    """
    Represents an <hr> HTML element (horizontal rule).

    This class is used to create horizontal lines for separating content sections in an HTML document.
    """

    def __init__(self):
        """
        Initializes an `Hr` object representing an HTML <hr> element.
        """
        super().__init__()

    def construct(self) -> str:
        """
        Converts the `Hr` object into an HTML <hr> element.

        Returns:
            str: The HTML string representing an <hr> element.
        """
        return "<hr>"


HorizontalLine = Hr()


class Spacer(HTMLElement):
    """
    Represents a flexible spacer `<div>` element that supports customizable margins.

    This class is used to create spacing in layouts with customizable top and bottom margins.
    """

    def __init__(self, margin_top: str = "1em", margin_bottom: str = "1em"):
        """
        Initializes a `Spacer` object with custom top and bottom margins.

        Args:
            margin_top (str): The margin-top value. Defaults to '1em'.
            margin_bottom (str): The margin-bottom value. Defaults to '1em'.
        """
        self.mt = margin_top
        self.mb = margin_bottom
        super().__init__()

    def construct(self) -> str:
        """
        Converts the `Spacer` object into an HTML `<div>` element with customizable margins.

        Returns:
            str: The HTML string representing a `<div>` element styled as a spacer.
        """
        return f'<div style="width: 100%; margin-top: {self.mt}; margin-bottom: {self.mb}"></div>'
