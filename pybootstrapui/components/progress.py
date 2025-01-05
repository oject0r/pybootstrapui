from .base import HTMLElement
from .dynamics.queue import add_task


class ProgressBar(HTMLElement):
    """
    Represents a Bootstrap progress bar component.

    Attributes:
        value (int): The current progress value (0-100).
        label (str | None): Optional label to display inside the progress bar.
        style (str): Bootstrap style (e.g., "primary", "success", "info", "warning", "danger").
        striped (bool): Whether the progress bar has a striped design. Defaults to `False`.
        animated (bool): Whether the progress bar has an animation. Defaults to `False`.
        classes (list[str] | None): Optional CSS classes for customization.
        id (str | None): Unique identifier for the progress bar.
    """

    def __init__(
        self,
        value: int,
        label: str | None = None,
        style: str = "primary",
        striped: bool = False,
        animated: bool = False,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes a `ProgressBar` object.

        Args:
            value (int): The current progress value (0-100).
            label (str | None): Optional label to display inside the progress bar.
            style (str): Bootstrap style (e.g., "primary", "success").
            striped (bool): Whether the progress bar has stripes.
            animated (bool): Whether the progress bar has animation.
            classes (list[str] | None): Optional CSS classes.
            id (str | None): Unique identifier.

        Example:
            progress_bar = ProgressBar(
                value=50,
                label="50% Complete",
                style="success",
                striped=True,
                animated=True,
                classes=["custom-progress"]
            )
        """
        super().__init__(classes, id)
        self.value = max(0, min(value, 100))  # Clamp value between 0 and 100
        self.label = label
        self.style = style
        self.striped = striped
        self.animated = animated

    def change_value(self, value: int, new_label: str = ""):
        """
        Updates the value and optionally the label of the progress bar.

        Args:
            value (int): The new progress value (0-100).
            new_label (str): Optional new label for the progress bar.

        Example:
            progress_bar.change_value(75, "75% Complete")
        """
        if new_label:
            self.label = new_label

        self.value = max(0, min(value, 100))
        add_task(
            f"{self.id}", "updateProgressBar", newValue=self.value, newText=self.label
        )

    def remove(self):
        """
        Removes the progress bar from the DOM.

        Note:
            - Triggers a task to remove the progress bar dynamically.
        """
        add_task(f"{self.id}HOST", "deleteElement")
        del self

    def construct(self) -> str:
        """
        Constructs the HTML representation of the progress bar.

        Returns:
            str: The HTML string representing the progress bar.

        Example:
            html = progress_bar.construct()
            print(html)
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
