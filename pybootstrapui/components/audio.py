from .base import HTMLElement
from pathlib import Path


class Audio(HTMLElement):
    """
    A class representing an HTML5 audio element with support for multiple sources.

    This class generates an <audio> element with specified sources, optional controls,
    and fallback text for unsupported environments.

    Attributes:
        sources (list[str]): A list of audio source URLs.
        controls (bool): Whether to display audio controls (default: True).
        classes (list[str] | None): CSS classes applied to the audio element.
        id (str | None): A unique identifier for the audio element.
    """

    def __init__(
        self,
        *sources: str,
        controls: bool = True,
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """
        Initializes the Audio element.

        Args:
            sources (list[str]): A list of audio source URLs.
            controls (bool): Whether to display audio controls (default: True).
            classes (list[str] | None): Optional CSS classes applied to the audio element.
            unique_id (str | None): Optional unique identifier for the audio element.

        Example:
            audio = Audio(
                sources=["audio1.mp3", "audio2.ogg"],
                controls=True,
                classes=["audio-player"]
            )
        """
        super().__init__(classes, unique_id)
        self.sources = sources
        self.controls = controls

    def construct(self) -> str:
        """
        Generates the HTML representation of the audio element.

        Returns:
            str: The HTML string for the <audio> element.

        Example:
            html = audio.construct()
            print(html)
        """
        sources_html = "\n".join(
            [
                f'<source src="{source}" type="audio/{Path(source).suffix.lstrip(".")}">'
                for source in self.sources
            ]
        )

        return f"""
        <audio{' controls' if self.controls else ''}>
            {sources_html}
            <p>
                Looks like this web engine doesn't support HTML5 audio.
                Consider upgrading to a modern browser engine (such as Blink/Webkit or Gecko).
                If you can't upgrade, here is an <a href="{self.sources[0]}">audio link</a>.
            </p>
        </audio>
        """
