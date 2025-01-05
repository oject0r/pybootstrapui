from .base import HTMLElement, RGBAColor
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
import warnings


class BootstrapIcon(HTMLElement):
    """
    A class representing a Bootstrap icon.

    This class generates an HTML <i> element with the specified Bootstrap icon class.

    Attributes:
            icon (str): The name of the Bootstrap icon.
    """

    def __init__(self, icon_name: str, color: RGBAColor | None = None):
        """
        Initializes a BootstrapIcon object with the specified icon name.

        Parameters:
                icon_name (str): The name of the Bootstrap icon.
        """
        super().__init__()
        self.icon = icon_name
        self.color = color

    def construct(self):
        """
        Generates the HTML code for the Bootstrap icon.

        Returns:
                str: The HTML code for the <i> element with the Bootstrap icon class.
        """

        style_attr = (
            f'style="color: {self.color.construct()};"' if self.color is not None
            else ''
        )

        return f'<i class="bi bi-{self.icon}" {style_attr}></i>'


class TextObject(HTMLElement):
    """
    A class representing a text element in HTML, with customizable properties such as font size, text type, and classes.

    This class generates HTML tags like <p>, <h1>, <a>, etc., with options for font size, classes, unique IDs, and hyperlinks.

    Attributes:
            label (str): The text content to display.
            size (int): The font size for the text (default is 18).
            id (str | None): The unique ID for the text element (optional).
            type (str): The type of HTML tag to use (default is 'p').
            href (str | None): The hyperlink target (only relevant if the text is a link).
    """

    def __init__(
        self,
        *text: str | BootstrapIcon,
        font_size: int = 18,
        color: RGBAColor | None = None,
        classes: list[str] | None = None,
        unique_id: str | None = None,
        text_type: str = "p",
        href: str | None = None,
        text_join: str = " ",
    ):
        """
        Initializes a TextObject with the specified properties.

        Parameters:
                label (str): The text content to display.
                font_size (int): The font size for the text (default is 18).
                classes (list[str] | None): Optional list of classes to apply to the element.
                unique_id (str | None): Optional unique ID for the element.
                text_type (str): The type of HTML tag to use (default is 'p').
                href (str | None): The URL for the hyperlink (relevant only for 'a' type).
        """
        super().__init__(classes, unique_id)
        self.label = text_join.join(
            i.construct() if isinstance(i, BootstrapIcon) else i for i in text
        )
        self.size = font_size
        self.type = text_type
        self.href = href
        self.color = color

    def construct(self):
        """
        Generates the HTML code for the text element.

        Returns:
                str: The HTML code for the text element with the specified properties.
        """
        self.label = self.label.replace("\n", "<br>")

        style_attr = (
            f'style="font-size: {self.size}px; color: {self.color.construct()};"' if self.color and self.size != 18
            else f'style="color: {self.color.construct()};"' if self.color and self.size == 18
            else f'style="font-size: {self.size}px;"' if self.size != 18
            else ''
        )

        classes_attr = f'class="{self.classes_str}"' if len(self.classes) > 0 else ''
        href_attr = f'href="{self.href}"' if self.href else ''


        return f"""
		<{self.type} {href_attr} {classes_attr} {f'id="{self.id}"' if self.id else ''}{style_attr}>{self.label}</{self.type}>
		"""


def bold(text: any, classes: list[str] | str = ""):
    """
    Creates a bold HTML element.

    Parameters:
            text (any): The text or content to be bolded.
            classes (list[str] | str): Optional list of classes to apply to the <b> element.

            Returns:
                    str: The HTML code for a <b> element containing the bolded text.
    """
    text = str(text)
    if type(classes) == list:
        classes = " ".join(classes)

    return f'<b class="{classes}">{text}</b>' if classes is "" else f'<b>{text}</b>'


def italic(text: str):
    """
    Creates an italic HTML element.

    Parameters:
            text (str): The text to be italicized.

            Returns:
                    str: The HTML code for an <i> element containing the italicized text.
    """
    text = str(text)
    return f"<i>{text}</i>"


class Text(TextObject):
    """
    A class representing a standard text element (<p>) with a default font size of 24px.

    Inherits from TextObject and applies a default font size.

    Attributes:
            label (str): The text content to display.
            classes (list[str] | None): Optional list of classes to apply to the element.
            id (str): Optional unique ID for the element.
    """

    def __init__(
        self,
        *text: str | BootstrapIcon,
        font_size: int = 18,
        color: RGBAColor | None = None,
        classes: list[str] | None = None,
        unique_id: str | None = None,
        text_join: str = " ",
    ):
        """
        Initializes a Text object.

        Parameters:
                label (str): The text content to display.
                classes (list[str] | None): Optional list of classes to apply to the element.
                unique_id (str | None): Optional unique ID for the element.
        """

        super().__init__(*text, font_size=font_size, color=color, classes=classes, unique_id=unique_id, text_join=text_join)


class Link(TextObject):
    """
    A class representing a hyperlink (<a>) element with customizable text content, font size, and target URL.

    Inherits from TextObject and sets the text type to 'a' for anchor links.

    Attributes:
            label (str): The text content to display for the link.
            href (str): The target URL for the link.
            classes (list[str] | None): Optional list of classes to apply to the element.
            unique_id (str | None): Optional unique ID for the element.
    """

    def __init__(
        self,
        *text: str | BootstrapIcon,
        href: str,
        font_size: int = 18,
        color: RGBAColor | None = None,
        classes: list[str] | None = None,
        unique_id: str | None = None,
        text_join: str = " ",
    ):
        """
        Initializes a Link object with the specified label, href, and optional styling.

        Parameters:
                label (str): The text content to display for the link.
                href (str): The target URL for the link.
                font_size (int): The font size for the link (default is 18).
                classes (list[str] | None): Optional list of classes to apply to the <a> element.
                unique_id (str | None): Optional unique ID for the <a> element.
        """
        super().__init__(*text, href=href, font_size=font_size, color=color, classes=classes, unique_id=unique_id, text_join=text_join)


class Header(TextObject):
    """
    A class representing a header element (h1, h2, etc.) with an optional Bootstrap icon.

    Inherits from TextObject and allows for the creation of headers with customizable size (1-6), icon, and other properties.

    Attributes:
            label (str): The text content for the header.
            header_size (int): The size of the header (1-6). Defaults to 1 (h1).
            classes (list[str] | None): Optional list of classes to apply to the header element.
            id (str | None): Optional unique ID for the header element.
    """

    def __init__(
        self,
        *text: str | BootstrapIcon,
        header_size: int = 1,
        bi: BootstrapIcon | None = None,
        color: RGBAColor | None = None,
        classes: list[str] | None = None,
        unique_id: str | None = None,
        text_join: str = " ",
    ):
        """
        Initializes a Header object with the specified properties.

        Parameters:
                label (str): The text content for the header.
                header_size (int): The size of the header (1-6), default is 1.
                bi (BootstrapIcon | None): An optional Bootstrap icon to display in the header.
                classes (list[str] | None): Optional list of classes to apply to the header element.
                unique_id (str | None): Optional unique ID for the header element.
        """

        text = list(text)
        if bi is not None:
            text.insert(0, bi)
            warnings.warn(
                "The 'bi' parameter in Header is deprecated. Please include it directly within the strings passed via *text.",
                DeprecationWarning,
                stacklevel=2
            )

        super().__init__(*text, classes=classes, color=color, unique_id=unique_id, text_type=f'h{header_size}', text_join=text_join)
        self.header_size = header_size


class Code(HTMLElement):
    def __init__(
        self,
        code: str,
        language: str = "auto",
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        super().__init__(classes, unique_id)
        self.code = code
        self.language = language

    def construct(self) -> str:
        """
        Construct an HTML representation of the code block with syntax highlighting.

        Returns:
                str: HTML string of the syntax-highlighted code block.
        """
        # Determine the appropriate lexer
        try:
            if self.language == "auto":
                lexer = guess_lexer(self.code)
            else:
                lexer = get_lexer_by_name(self.language)
        except Exception as e:
            # Fallback to a generic text lexer if detection fails
            lexer = get_lexer_by_name("text")

        # Create an HTML formatter
        formatter = HtmlFormatter(nowrap=True)

        # Highlight the code
        highlighted_code = highlight(self.code, lexer, formatter)

        # Prepare class and id attributes
        class_attr = f'class="highlight {self.classes_str}"'
        id_attr = f'id="{self.id}"' if self.id else ""

        # Construct the final HTML
        return f"<pre {id_attr} {class_attr}>{highlighted_code}</pre>"
