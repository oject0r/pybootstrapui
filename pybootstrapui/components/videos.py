import os
from pathlib import Path
from .base import HTMLElement


class Video(HTMLElement):
	"""
    Represents an HTML `<video>` element that supports multiple video sources,
    optional controls, and a poster image.

    Attributes:
        sources (list[str]): A list of video source URLs.
        controls (bool): Whether to display video controls. Default is `True`.
        width (int): The width of the video element. Default is `640`.
        height (int): The height of the video element. Default is `264`.
        poster (str | None): URL of the poster image displayed before playback starts.
        classes (list[str] | None): CSS classes applied to the video element.
        id (str | None): A unique identifier for the video element.
    """

	def __init__(
			self,
			source: str | list[str],
			*,
			controls: bool = True,
			width: int = 640,
			height: int = 264,
			poster_source: str | None = None,
			classes: list[str] | None = None,
			unique_id: str | None = None,
	):
		"""
        Initializes a `Video` element.

        Args:
            source (str | list[str]): A single video source URL or a list of video sources.
            controls (bool): Whether to display video controls. Default is `True`.
            width (int): The width of the video element. Default is `640`.
            height (int): The height of the video element. Default is `264`.
            poster_source (str | None): URL of the poster image displayed before playback starts. Default is `None`.
            classes (list[str] | None): CSS classes applied to the video element. Default is `None`.
            unique_id (str | None): A unique identifier for the video element. Default is `None`.

        Raises:
            FileNotFoundError: If one or more video sources do not exist.

        Example:
            video = Video(
                source=["video1.mp4", "video2.webm"],
                controls=True,
                width=800,
                height=450,
                poster_source="poster.png",
                classes=["video-responsive"]
            )
        """
		super().__init__(classes, unique_id)

		if isinstance(source, list):
			if not all(os.path.exists(src) for src in source):
				missing = [src for src in source if not os.path.exists(src)]
				raise FileNotFoundError(
					f"Files do not exist: {', '.join(missing).strip(', ')}"
				)
			self.sources = source
		else:
			if not os.path.exists(source):
				raise FileNotFoundError(f"File does not exist: {source}")
			self.sources = [source]

		self.controls = controls
		self.width = width
		self.height = height
		self.poster = poster_source

	def construct(self) -> str:
		"""
        Constructs the HTML representation of the video element.

        Returns:
            str: The HTML string for the video element.

        Example:
            html = video.construct()
            print(html)
        """
		sources_html = "\n".join(
			[
				f'<source src="{source}" type="video/{Path(source).suffix.lstrip(".")}">'
				for source in self.sources
			]
		)
		poster_html = f'poster="{self.poster}"' if self.poster else ""
		id_attr = f'id="{self.id}"' if self.id else ""
		class_attr = f'class="video-js {self.classes_str}"' if self.classes_str else ""

		return f"""
        <video {id_attr} {class_attr}
            {'controls' if self.controls else ''}
            width="{self.width}" height="{self.height}"
            {poster_html}
            data-setup="{{}}"
        >
            {sources_html}
            <p class="vjs-no-js">
                Looks like JavaScript is disabled. Enable JavaScript or 
                <a href="https://videojs.com/html5-video-support/" target="_blank">upgrade your browser</a>.
                <br>For <b class="gradient-text">PyBootstrapUI</b>, check NW.js setup or package.json settings.
            </p>
        </video>
        """
