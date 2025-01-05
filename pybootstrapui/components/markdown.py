from .base import HTMLElement
import markdown


class Markdown(HTMLElement):
    """
    A class representing a Markdown content element.

    This class converts a Markdown string into HTML using the markdown_source library
    and can be integrated as an HTML element.

    Attributes:
            - src (str): The source Markdown content.
            - unique_id (str | None): Optional unique ID for the element.
            - classes (list[str] | None): Optional list of classes to apply to the element.
    """

    def __init__(
        self,
        markdown_source: str,
        unique_id: str | None = None,
        classes: list[str] | None = None,
    ):
        """
        Initializes the Markdown object with the source Markdown content.

        Parameters:
                - markdown_source (str): The Markdown content to be rendered.
                - unique_id (str | None): Optional unique ID for the element.
                - classes (list[str] | None): Optional list of CSS classes to apply to the element.

        Example:
                
                markdown_element = Markdown("# Heading\nThis is a paragraph.", classes=["markdown_source-content"])
                
        """
        super().__init__(classes, unique_id)
        self.src = markdown_source

    def construct(self) -> str:
        """
        Converts the Markdown content into HTML.

        Returns:
                - str: The rendered HTML content.

        Example:
                
                html = markdown_element.construct()
                print(html)
                
        """
        html_content = markdown.markdown(self.src, output_format="html")
        class_attr = f'class="{self.classes_str}"' if self.classes_str else ""
        id_attr = f'id="{self.id}"' if self.id else ""
        return f"<div {class_attr} {id_attr}>{html_content}</div>"
