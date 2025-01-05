from .base import HTMLElement
from .text import Header
from .images import ImageObject, URLImage


class Card(HTMLElement):
    """
    A class to generate a card component with optional header, footer, image, and child elements.

    Attributes:
            header (Header | None): An optional header for the card.
            footer (list[HTMLElement] | None): An optional list of elements for the card footer.
            image (str | None): An optional URL for the card's image.
            children (list[HTMLElement]): A list of child elements to be included in the card body.
    """

    def __init__(
        self,
        children: list[HTMLElement],
        header: Header | None = None,
        footer: list[HTMLElement] | None = None,
        image: ImageObject | URLImage | None = None,
        unique_id: str | None = None,
        classes: list[str] | None = None,
    ) -> None:
        """
        Initializes the Card with optional header, footer, image, and child elements.

        Parameters:
                children (list[HTMLElement]): The child elements to be included inside the card.
                header (Header | None): An optional header for the card.
                footer (list[HTMLElement] | None): An optional list of elements for the card footer.
                image (ImageObject | URLImage | None): An optional URL for the card's image.
                unique_id (str | None): An optional unique ID for the card.
                classes (list[str] | None): Optional list of CSS classes for styling the card.

        Example:
                # Create a card with a header, footer, image, and child elements
                card = Card(
                        children=[Text("Card content"), button],
                        header=Header("Card Header"),
                        footer=[Text("Card Footer"), link],
                        image=URLImage("https://example.com/image.jpg"),
                        classes=["custom-card"]
                )

        Note:
                - The classes parameter allows adding custom CSS styles.
                - If header is provided, it will be rendered at the top of the card.
                - If footer is provided, it will be rendered at the bottom of the card.
                - If image is provided, it will be displayed at the top of the card.
        """
        super().__init__(classes, unique_id)
        self.header = header
        self.footer = footer
        self.image = image
        self.children = children

    def construct(self) -> str:
        """
        Generates the HTML code for the card, including its header, body, footer, and image (if provided).

        Returns:
                str: The HTML code for the card element.

        Example:
                # Render the card into HTML
                html = card.construct()
        """
        header_html = (
            f'<div class="card-header">{self.header.construct()}</div>'
            if self.header
            else ""
        )
        footer_html = (
            f'<div class="card-footer">{"".join([element.construct() for element in self.footer])}</div>'
            if self.footer
            else ""
        )

        if self.image:
            self.image.add_class("card-img-top")

        image_html = self.image.construct() if self.image else ""
        body_html = "\n".join([child.construct() for child in self.children])

        return f"""
		<div class="card mb-4" id="{self.id}" class="{self.classes_str}">
			{header_html}
			{image_html}
			<div class="card-body">
				{body_html}
			</div>
			{footer_html}
		</div>
		"""
