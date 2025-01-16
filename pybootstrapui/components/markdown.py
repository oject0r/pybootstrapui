from .base import HTMLElement


class Markdown(HTMLElement):
    """
    Represents a Markdown content element.

    This class converts a Markdown string into HTML using the `markdown` library
    and integrates it as an HTML element.

    Attributes:
        src (str): The source Markdown content.
        id (str | None): Optional unique ID for the element.
        classes (list[str] | None): Optional list of CSS classes to apply to the element.
    """

    def __init__(
        self,
        markdown_source: str,
        id: str | None = None,
        classes: list[str] | None = None,
    ):
        """
        Initializes the `Markdown` object with the source Markdown content.

        Args:
            markdown_source (str): The Markdown content to be rendered.
            id (str | None): Optional unique ID for the element.
            classes (list[str] | None): Optional list of CSS classes to apply to the element.

        Example:
            markdown_element = Markdown(
                "# Heading\nThis is a paragraph.",
                classes=["markdown-content"]
            )
        """

        super().__init__(classes, id)
        self.src = markdown_source

    def construct(self) -> str:
        """
        Converts the Markdown content into HTML.

        Returns:
            str: The rendered HTML content.

        Example:
            html = markdown_element.construct()
            print(html)
        """


        try:
            import markdown
        except ImportError:
            raise ModuleNotFoundError('To use markdown objects please install markdown via pip:\npip install markdown')


        html_content = markdown.markdown(self.src, output_format="html")
        class_attr = f'class="{self.classes_str}"' if self.classes_str else ""
        id_attr = f'id="{self.id}"' if self.id else ""
        return f"<div {class_attr} {id_attr}>{html_content}</div>"
