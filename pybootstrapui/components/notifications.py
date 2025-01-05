from .base import HTMLElement
from pybootstrapui.components.dynamics.queue import add_task


class Notification(HTMLElement):
    """
    Represents a notification (alert) component.

    Attributes:
        message (str): The text content of the notification.
        style (str): The style of the notification (e.g., "success", "info", "warning", "danger").
        dismissable (bool): Whether the notification can be dismissed. Defaults to `True`.
        classes (list[str] | None): Additional CSS classes for styling.
        id (str | None): Unique identifier for the notification.
    """

    def __init__(
        self,
        message: str,
        style: str = "info",
        dismissable: bool = True,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes a `Notification` object.

        Args:
            message (str): The text content of the notification.
            style (str): The style of the notification (e.g., "success", "info", "warning", "danger").
            dismissable (bool): Whether the notification can be dismissed.
            classes (list[str] | None): Additional CSS classes for styling.
            id (str | None): Optional unique identifier for the notification.

        Example:
            notification = Notification(
                message="Operation completed successfully.",
                style="success",
                dismissable=True,
                classes=["custom-alert"]
            )
        """
        super().__init__(classes, id)
        self.message = message
        self.style = style
        self.dismissable = dismissable

    def construct(self) -> str:
        """
        Constructs the HTML representation of the notification.

        Returns:
            str: The HTML string for the notification component.

        Example:
            html = notification.construct()
            print(html)
        """
        dismiss_button = ""
        if self.dismissable:
            dismiss_button = '<button type="button" class="btn-close" aria-label="Close" onclick="this.parentElement.remove();"></button>'

        return f"""
        <div id="{self.id}" class="alert alert-{self.style} {'alert-dismissible fade show' if self.dismissable else ''}" role="alert">
            {self.message}
            {dismiss_button}
        </div>
        """

    def dismiss(self):
        """
        Dismisses the notification dynamically on the client.

        Note:
            - Triggers a task to remove the notification element from the DOM.
        """
        add_task(self.id, "deleteElement")
