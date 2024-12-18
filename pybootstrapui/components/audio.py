from .base import HTMLElement
from pathlib import Path


class Audio(HTMLElement):
	def __init__(self, sources: list[str], controls: bool = True, classes: list[str] | None = None, unique_id: str | None = None):
		super().__init__(classes, unique_id)
		self.sources = sources
		self.controls = controls

	def construct(self) -> str:

		sources_html = '\n'.join([
			f'<source src="{source}" type="video/{Path(source).suffix.lstrip(".")}">'
			for source in self.sources
		])

		return f'''
		<audio{' controls' if self.controls else ''}>
			{sources_html}
			  <p>
				Looks like that this web engine doesn't support HTML5 audio.
				Consider yourself upgrading a better and advanced engine (such as new Blink/Webkit or new Gecko).
				If you can't upgrade, here is an <a href="{self.sources[0]}">audio link.</a>
			  </p>
		</audio>
		'''
