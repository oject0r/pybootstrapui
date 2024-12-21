from .base import HTMLElement
from pybootstrapui.components.dynamics.queue import add_task


class Notification(HTMLElement):
	"""
	A class representing a notification (alert) component.

	Attributes:
		- `message` (str): The text content of the notification.
		- `style` (str): The style of the notification (e.g., "success", "info", "warning", "danger").
		- `dismissable` (bool): Whether the notification can be dismissed (default: True).
	"""

	def __init__(self, message: str, style: str = "info", dismissable: bool = True, classes: list[str] | None = None, unique_id: str | None = None):
		"""
		Initializes a notification.

		Parameters:
			- `message` (str): The text content of the notification.
			- `style` (str): The style of the notification (e.g., "success", "info").
			- `dismissable` (bool): Whether the notification can be dismissed.
			- `classes` (list[str] | None): Additional CSS classes.
			- `unique_id` (str | None): Optional unique identifier.
		"""
		super().__init__(classes, unique_id)
		self.message = message
		self.style = style
		self.dismissable = dismissable

	def construct(self) -> str:
		"""
		Constructs the HTML representation of the notification.

		Returns:
			- `str`: The HTML string.
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
		"""
		add_task(self.id, "deleteElement")
