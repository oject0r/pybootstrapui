from .base import HTMLElement
from pybootstrapui.components.dynamics.queue import add_task
from typing import Literal


class Tooltip(HTMLElement):
    """
    Represents a Bootstrap tooltip component.

    Tooltips are used to display additional information when users hover over, focus on,
    or tap an element.

    Attributes:
        target (HTMLElement | str): The target element for the tooltip. Can be an `HTMLElement` object or an element ID.
        content (str): The text content displayed within the tooltip.
        placement (Literal["top", "bottom", "left", "right"]): The position of the tooltip relative to the target. Default is `"top"`.
        classes (list[str] | None): Additional CSS classes for the tooltip container.
        id (str | None): A unique identifier for the tooltip.
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
        Initializes a `Tooltip` object with a target, content, and optional parameters.

        Args:
            target (HTMLElement | str): The target element or its unique ID where the tooltip will be attached.
            content (str): The text content of the tooltip.
            placement (Literal["top", "bottom", "left", "right"]): Tooltip placement relative to the target. Default is `"top"`.
            auto_attach (bool): Whether to automatically attach the tooltip during initialization. Default is `True`.
            classes (list[str] | None): Additional CSS classes for the tooltip.
            unique_id (str | None): Optional unique identifier for the tooltip.

        Example:
            tooltip = Tooltip(
                target="button1",
                content="This is a tooltip",
                placement="bottom"
            )
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

        This method creates a dynamic task to attach the tooltip on the frontend.

        Example:
            tooltip.attach()
        """
        target_id = (
            self.target.id if isinstance(self.target, HTMLElement) else self.target
        )
        add_task(
            target_id, "addTooltip", content=self.content, placement=self.placement
        )

    def construct(self) -> str:
        """
        Generates the HTML and JavaScript initialization code for the tooltip.

        Returns:
            str: The JavaScript snippet for initializing the tooltip.

        Example:
            html = tooltip.construct()
            print(html)
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
