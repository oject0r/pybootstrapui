from .base import HTMLElement, RGBAColor
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
import warnings


class BootstrapIcon(HTMLElement):
    """
    Represents a Bootstrap icon component.

    Attributes:
        icon (str): The name of the Bootstrap icon.
        color (RGBAColor | None): Optional RGBA color for the icon.
    """

    def __init__(self, icon_name: str, color: RGBAColor | None = None):
        """
        Initializes a `BootstrapIcon` object with the specified icon name.

        Args:
            icon_name (str): The name of the Bootstrap icon.
            color (RGBAColor | None): Optional RGBA color for the icon.

        Example:
            icon = BootstrapIcon("check-circle", RGBAColor(255, 0, 0, 0.5))
        """
        super().__init__()
        self.icon = icon_name
        self.color = color

    def construct(self) -> str:
        """
        Generates the HTML code for the Bootstrap icon.

        Returns:
            str: The HTML code for the `<i>` element with the Bootstrap icon class.

        Example:
            html = icon.construct()
            print(html)
        """
        style_attr = (
            f'style="color: {self.color.construct()};"' if self.color is not None else ""
        )
        return f'<i class="bi bi-{self.icon}" {style_attr}></i>'


class TextObject(HTMLElement):
    """
    Represents a customizable text element in HTML.

    Attributes:
        label (str): The text content to display.
        size (int): The font size of the text (default is 18).
        type (str): The type of HTML tag to use (e.g., 'p', 'h1', 'a').
        href (str | None): The hyperlink target (only applicable for 'a' tag).
        color (RGBAColor | None): Optional RGBA color for the text.
        classes (list[str] | None): Additional CSS classes.
        id (str | None): Optional unique identifier for the text element.
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
        Initializes a `TextObject` with customizable properties.

        Args:
            text (str | BootstrapIcon): Text content or Bootstrap icons.
            font_size (int): Font size of the text (default is 18).
            color (RGBAColor | None): Optional RGBA color for the text.
            classes (list[str] | None): Additional CSS classes.
            unique_id (str | None): Optional unique identifier for the text element.
            text_type (str): The HTML tag type (default is 'p').
            href (str | None): Hyperlink target if text_type is 'a'.
            text_join (str): String used to join text or icons.

        Example:
            text_obj = TextObject(
                "Hello", BootstrapIcon("star"), font_size=20, color=RGBAColor(0, 128, 255, 1)
            )
        """
        super().__init__(classes, unique_id)
        self.label = text_join.join(
            i.construct() if isinstance(i, BootstrapIcon) else i for i in text
        )
        self.size = font_size
        self.type = text_type
        self.href = href
        self.color = color

    def construct(self) -> str:
        """
        Generates the HTML code for the text element.

        Returns:
            str: The HTML code for the text element.

        Example:
            html = text_obj.construct()
            print(html)
        """
        self.label = self.label.replace("\n", "<br>")
        style_attr = (
            f'style="font-size: {self.size}px; color: {self.color.construct()};"'
            if self.color and self.size != 18
            else f'style="color: {self.color.construct()};"'
            if self.color
            else f'style="font-size: {self.size}px;"'
            if self.size != 18
            else ""
        )

        classes_attr = f'class="{self.classes_str}"' if self.classes else ""
        href_attr = f'href="{self.href}"' if self.href else ""

        return f"""
        <{self.type} {href_attr} {classes_attr} {f'id="{self.id}"' if self.id else ''} {style_attr}>
            {self.label}
        </{self.type}>
        """


def bold(text: any, classes: list[str] | str = "") -> str:
    """
    Creates a bold HTML element.

    Args:
        text (any): The text or content to make bold.
        classes (list[str] | str): Additional CSS classes (optional).

    Returns:
        str: The HTML code for a `<b>` element containing the bolded text.

    Example:
        bold_text = bold("Important", ["highlight"])
    """
    text = str(text)
    if isinstance(classes, list):
        classes = " ".join(classes)

    return (
        f'<b class="{classes}">{text}</b>' if classes else f'<b>{text}</b>'
    )


def italic(text: str) -> str:
    """
    Creates an italic HTML element.

    Args:
        text (str): The text to be italicized.

    Returns:
        str: The HTML code for an `<i>` element containing the italicized text.

    Example:
        italic_text = italic("Emphasis")
    """
    return f"<i>{text}</i>"


class Text(TextObject):
    """
    Represents a standard text element with a default font size of 18px.

    Inherits from `TextObject` and applies default text properties.

    Attributes:
        label (str): The text content to display.
        classes (list[str] | None): Additional CSS classes.
        id (str | None): Unique identifier for the text element.
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
        Initializes a `Text` object.

        Args:
            text (str | BootstrapIcon): Text content or icons.
            font_size (int): Font size of the text.
            color (RGBAColor | None): RGBA color for the text.
            classes (list[str] | None): Additional CSS classes.
            unique_id (str | None): Unique identifier for the text element.

        Example:
            text = Text("Sample Text", font_size=24)
        """
        super().__init__(
            *text,
            font_size=font_size,
            color=color,
            classes=classes,
            unique_id=unique_id,
            text_join=text_join,
        )


from .base import HTMLElement, RGBAColor
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
import warnings


class Link(TextObject):
    """
    Represents a hyperlink (`<a>` element) with customizable text content, font size, and target URL.

    Inherits from `TextObject` and sets the `text_type` to `'a'` for anchor links.

    Attributes:
        href (str): The target URL for the hyperlink.
        font_size (int): Font size of the text (default is 18).
        color (RGBAColor | None): Optional RGBA color for the text.
        classes (list[str] | None): Additional CSS classes for styling.
        id (str | None): Unique identifier for the hyperlink.
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
        Initializes a `Link` object.

        Args:
            text (str | BootstrapIcon): Text content or Bootstrap icons.
            href (str): The target URL for the hyperlink.
            font_size (int): Font size of the text (default is 18).
            color (RGBAColor | None): Optional RGBA color for the text.
            classes (list[str] | None): Additional CSS classes.
            unique_id (str | None): Unique identifier for the hyperlink.
            text_join (str): String used to join text or icons.

        Example:
            link = Link(
                "Click here",
                href="https://example.com",
                font_size=16,
                classes=["link-primary"]
            )
        """
        super().__init__(
            *text,
            href=href,
            font_size=font_size,
            color=color,
            classes=classes,
            unique_id=unique_id,
            text_join=text_join,
        )


class Header(TextObject):
    """
    Represents a header element (`<h1>` to `<h6>`) with optional text content and icons.

    Inherits from `TextObject` and allows setting header size and an optional Bootstrap icon.

    Attributes:
        header_size (int): The size of the header (1-6). Defaults to `1` (`<h1>`).
        color (RGBAColor | None): Optional RGBA color for the text.
        classes (list[str] | None): Additional CSS classes for styling.
        id (str | None): Unique identifier for the header.
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
        Initializes a `Header` object.

        Args:
            text (str | BootstrapIcon): Text content or Bootstrap icons.
            header_size (int): Header size (`1-6`). Default is `1` (`<h1>`).
            bi (BootstrapIcon | None): An optional Bootstrap icon.
            color (RGBAColor | None): Optional RGBA color for the text.
            classes (list[str] | None): Additional CSS classes.
            unique_id (str | None): Unique identifier for the header.
            text_join (str): String used to join text or icons.

        Warning:
            The `bi` parameter is deprecated. Please include the icon directly in the `*text` argument.

        Example:
            header = Header(
                "Welcome",
                header_size=2,
                color=RGBAColor(255, 0, 0, 1),
                classes=["text-center"]
            )
        """
        text = list(text)
        if bi is not None:
            text.insert(0, bi)
            warnings.warn(
                "The 'bi' parameter in Header is deprecated. Please include it directly within the strings passed via *text.",
                DeprecationWarning,
                stacklevel=2,
            )

        super().__init__(
            *text,
            classes=classes,
            color=color,
            unique_id=unique_id,
            text_type=f"h{header_size}",
            text_join=text_join,
        )
        self.header_size = header_size


class Code(HTMLElement):
    """
    Represents a syntax-highlighted code block in HTML.

    Attributes:
        code (str): The code content to display.
        language (str): The programming language for syntax highlighting (`auto` for automatic detection).
        classes (list[str] | None): Additional CSS classes for styling.
        id (str | None): Unique identifier for the code block.
    """

    def __init__(
        self,
        code: str,
        language: str = "auto",
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """
        Initializes a `Code` object.

        Args:
            code (str): The code content to display.
            language (str): Programming language for syntax highlighting (`auto` for automatic detection).
            classes (list[str] | None): Additional CSS classes.
            unique_id (str | None): Unique identifier for the code block.

        Example:
            code_block = Code(
                "print('Hello, World!')",
                language="python",
                classes=["code-block"]
            )
        """
        super().__init__(classes, unique_id)
        self.code = code
        self.language = language

    def construct(self) -> str:
        """
        Constructs the HTML representation of the code block with syntax highlighting.

        Returns:
            str: The HTML code block with syntax highlighting.

        Example:
            html = code_block.construct()
            print(html)
        """
        # Determine the appropriate lexer
        try:
            if self.language == "auto":
                lexer = guess_lexer(self.code)
            else:
                lexer = get_lexer_by_name(self.language)
        except Exception:
            # Fallback to a generic text lexer if detection fails
            lexer = get_lexer_by_name("text")

        # Create an HTML formatter
        formatter = HtmlFormatter(nowrap=True)

        # Highlight the code
        highlighted_code = highlight(self.code, lexer, formatter)

        # Prepare class and id attributes
        class_attr = f'class="highlight {self.classes_str}"' if self.classes_str else ""
        id_attr = f'id="{self.id}"' if self.id else ""

        return f"<pre {id_attr} {class_attr}>{highlighted_code}</pre>"
