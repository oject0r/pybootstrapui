from .base import HTMLElement
from pybootstrapui.components.dynamics.queue import add_task
from typing import Literal


class Tooltip(HTMLElement):
    """
    A class representing a Bootstrap tooltip.

    Attributes:
            - target (HTMLElement | str): The target element for the tooltip. It can be an HTMLElement or an element ID.
            - content (str): The text content of the tooltip.
            - placement (str): The position of the tooltip relative to the target (e.g., "top", "bottom", "left", "right").
    """

    def __init__(
        self,
        target: HTMLElement | str,
        content: str,
        placement: Literal["top", "bottom", "left", "right"] = "top",
        auto_attach: bool = True,
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """
        Initializes a tooltip.

        Parameters:
                - target (HTMLElement | str): Target element or its ID.
                - content (str): Text for the tooltip.
                - placement (str): Position of the tooltip ("top", "bottom", "left", "right").
                - classes (list[str] | None): Additional CSS classes.
                - unique_id (str | None): Optional unique identifier.
        """
        super().__init__(classes, unique_id)
        self.target = target
        self.content = content
        self.placement = placement

        if auto_attach:
            self.attach()

    def attach(self):
        """
        Attaches the tooltip to the target element dynamically.
        """
        target_id = (
            self.target.id if isinstance(self.target, HTMLElement) else self.target
        )
        add_task(
            target_id, "addTooltip", content=self.content, placement=self.placement
        )

    def construct(self) -> str:
        """
        Generates the HTML initialization code for the tooltip.

        Returns:
                - str: HTML string for initializing the tooltip.
        """
        target_id = (
            self.target.id if isinstance(self.target, HTMLElement) else self.target
        )
        return f"""
		<script>
			const tooltipTrigger = document.getElementById("{target_id}");
			if (tooltipTrigger) {{
				const tooltip = new bootstrap.Tooltip(tooltipTrigger, {{
					title: "{self.content}",
					placement: "{self.placement}"
				}});
			}}
		</script>
		"""
