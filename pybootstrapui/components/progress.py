from .base import HTMLElement
from .dynamics.queue import add_task


class ProgressBar(HTMLElement):
    """
    A class representing a Bootstrap progress bar.

    Attributes:
            - value (int): The current progress value (0-100).
            - label (str | None): Optional label to display inside the progress bar.
            - style (str): Bootstrap style (e.g., "success", "info", "warning", "danger").
            - striped (bool): Whether the progress bar is striped (default: False).
            - animated (bool): Whether the progress bar is animated (default: False).
    """

    def __init__(
        self,
        value: int,
        label: str | None = None,
        style: str = "primary",
        striped: bool = False,
        animated: bool = False,
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """
        Initializes the progress bar.

        Parameters:
                - value (int): The current progress value (0-100).
                - label (str | None): Optional label to display inside the progress bar.
                - style (str): Bootstrap style (e.g., "primary", "success").
                - striped (bool): Whether the progress bar is striped.
                - animated (bool): Whether the progress bar is animated.
                - classes (list[str] | None): Optional CSS classes.
                - unique_id (str | None): Unique identifier.
        """
        super().__init__(classes, unique_id)
        self.value = max(0, min(value, 100))  # Clamp value between 0 and 100
        self.label = label
        self.style = style
        self.striped = striped
        self.animated = animated

    def change_value(self, value: int, new_label: str = ""):
        if new_label:
            self.label = new_label

        self.value = max(0, min(value, 100))
        add_task(
            f"{self.id}", "updateProgressBar", newValue=self.value, newText=self.label
        )

    def remove(self):
        """
        Removes the progress bar from the DOM.
        """

        add_task(f"{self.id}HOST", "deleteElement")
        del self

    def construct(self) -> str:
        """
        Constructs the HTML representation of the progress bar.

        Returns:
                - str: HTML string.
        """
        progress_classes = f"progress-bar bg-{self.style}"
        if self.striped:
            progress_classes += " progress-bar-striped"
        if self.animated:
            progress_classes += " progress-bar-animated"

        label_html = f"{self.label}" if self.label else ""
        return f"""
		<div class="progress {self.classes_str}" id="{self.id}HOST" role="progressbar" aria-valuenow="{self.value}" aria-valuemin="0" aria-valuemax="100">
		  <div class="{progress_classes}" id="{self.id}" style="width: {self.value}%">{label_html}</div>
		</div>
		"""
