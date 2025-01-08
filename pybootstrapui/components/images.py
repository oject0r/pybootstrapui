from .base import HTMLElement
from os import PathLike
from pathlib import Path
import base64
import aiofiles


class ImageObject(HTMLElement):
    """
    Represents a base64-encoded image element for use in an HTML page.

    Attributes:
        data (str): Base64-encoded image data.
        width (str): The width of the image (default is 'auto').
        height (str): The height of the image (default is 'auto').
        alt (str): Alternative text for the image.
        classes (list[str] | None): CSS classes to apply to the image.
        id (str | None): Unique identifier for the image element.
    """

    def __init__(
        self,
        base64_data: bytes | str,
        *,
        width: str = "auto",
        height: str = "auto",
        alt: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes an ImageObject.

        Args:
            base64_data (bytes | str): The base64-encoded image data.
            width (str): The width of the image (default is 'auto').
            height (str): The height of the image (default is 'auto').
            alt (str | None): Alternative text for the image.
            classes (list[str] | None): CSS classes to apply to the image.
            id (str | None): Unique identifier for the image element.
        """
        super().__init__(classes, id)

        if isinstance(base64_data, bytes):
            base64_data = base64_data.decode(encoding="utf-8")

        self.data = base64_data
        self.width = width
        self.height = height
        self.alt = alt or "Image"

    def construct(self) -> str:
        """
        Constructs the HTML representation of the image.

        Returns:
            str: The HTML string for the image.
        """
        return f"""
        <img src="data:image/png;base64, {self.data}"
        {f'alt="{self.alt}"' if self.alt else ''}
        width="{self.width}" height="{self.height}"
        />
        """


class FileImage(ImageObject):
    """
    Represents an image loaded from a file and encoded as base64.
    """

    def __init__(
        self,
        file_path: str | bytes | PathLike[str] | PathLike[bytes],
        *,
        width: str = "auto",
        height: str = "auto",
        alt: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes a FileImage.

        Args:
            file_path (str | bytes | PathLike): Path to the image file.
            width (str): The width of the image (default is 'auto').
            height (str): The height of the image (default is 'auto').
            alt (str | None): Alternative text for the image.
            classes (list[str] | None): CSS classes to apply to the image.
            id (str | None): Unique identifier for the image element.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File with path {file_path} doesn't exist!")

        if not path.is_absolute():
            path = path.absolute()

        with open(path, "rb") as f:
            content = base64.b64encode(f.read())

        super().__init__(
            content,
            width=width,
            height=height,
            alt=alt,
            classes=classes,
            id=id,
        )


class RawImage(ImageObject):
    """
    Represents an image from raw binary data, which is encoded to base64.
    """

    def __init__(
        self,
        image_content: bytes,
        *,
        width: str = "auto",
        height: str = "auto",
        alt: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes a RawImage.

        Args:
            image_content (bytes): The raw binary data of the image.
            width (str): The width of the image (default is 'auto').
            height (str): The height of the image (default is 'auto').
            alt (str | None): Alternative text for the image.
            classes (list[str] | None): CSS classes to apply to the image.
            id (str | None): Unique identifier for the image element.
        """
        content = base64.b64encode(image_content).decode("utf-8")
        super().__init__(
            content,
            width=width,
            height=height,
            alt=alt,
            classes=classes,
            id=id,
        )


class URLImage(HTMLElement):
    """
    Represents an image loaded from a URL.

    Attributes:
        url (str): The URL of the image.
        width (str): The width of the image (default is 'auto').
        height (str): The height of the image (default is 'auto').
        alt (str): Alternative text for the image.
        classes (list[str] | None): CSS classes to apply to the image.
        id (str | None): Unique identifier for the image element.
    """

    def __init__(
        self,
        image_url: str,
        *,
        width: str = "auto",
        height: str = "auto",
        alt: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes a URLImage.

        Args:
            image_url (str): The URL of the image.
            width (str): The width of the image (default is 'auto').
            height (str): The height of the image (default is 'auto').
            alt (str | None): Alternative text for the image.
            classes (list[str] | None): CSS classes to apply to the image.
            id (str | None): Unique identifier for the image element.
        """
        self.url = image_url
        self.width = width
        self.height = height
        self.alt = alt or "Image"
        super().__init__(classes, id)

    def construct(self) -> str:
        """
        Constructs the HTML representation of the URL image.

        Returns:
            str: The HTML string for the image element.
        """
        return f"""
        <img src="{self.url}"
        {f'alt="{self.alt}"' if self.alt else ''}
        width="{self.width}" height="{self.height}"
        />
        """



async def image_from_file_async(
    file_path: str | bytes | PathLike[str] | PathLike[bytes],
    *,
    width: str = "auto",
    height: str = "auto",
    alt: str | None = None,
    classes: list[str] | None = None,
    unique_id: str | None = None,
) -> ImageObject:
    """Asynchronously creates an ImageObject from
    a file.

    Parameters:
        - file_path (str | bytes | PathLike): The path to the image file.
        - width (str): The width of the image (default is 'auto').
        - height (str): The height of the image (default is 'auto').
        - alt (str | None): Alternative text for the image.
        - classes (list[str] | None): CSS classes to apply to the image.
        - unique_id (str | None): Unique identifier for the image element.

    Returns:
        - ImageObject: An instance of ImageObject containing the base64-encoded image.

    Raises:
        - FileNotFoundError: If the file at the given path does not exist.

    Example:
        image = await image_from_file_async("path/to/image.png", width="100px")
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File with path {file_path} doesn't exist!")

    if not path.is_absolute():
        path = path.absolute()

    async with aiofiles.open(path, "rb") as f:
        content = base64.b64encode(await f.read())

    return ImageObject(
        content,
        width=width,
        height=height,
        alt=alt,
        classes=classes,
        id=unique_id,
    )
