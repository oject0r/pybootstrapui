from .base import HTMLElement


class CustomHTML(HTMLElement):
    """
    A class representing a custom HTML element.

    This class allows for inserting raw HTML content into the DOM, bypassing other structured components.

    Attributes:
        content (str): The raw HTML content to be included.

    Warning:
        Using raw HTML can pose security risks (e.g., XSS attacks) if the content is not sanitized.
        Ensure that the provided HTML is safe and valid.
    """

    def __init__(self, content: str):
        """
        Initializes a CustomHTML object with the specified raw HTML content.

        Args:
            content (str): The raw HTML content to be included.

        Example:
            # Create a custom HTML component
            custom_html = CustomHTML('<div class="custom">Hello, World!</div>')
        """
        super().__init__()
        self.content = content

    def construct(self) -> str:
        """
        Generates the raw HTML content.

        Returns:
            str: The raw HTML content.

        Example:
            # Render the custom HTML
            html = custom_html.construct()
        """
        return self.content
