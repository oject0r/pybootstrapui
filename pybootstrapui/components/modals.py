from .base import HTMLElement
from pybootstrapui.components.dynamics.queue import add_task


class Modal(HTMLElement):
    """
    Represents a Bootstrap modal component.

    This class provides methods for constructing, displaying, and hiding modal windows.

    Attributes:
        title (str | None): The modal's title.
        body (list[HTMLElement]): Child elements within the modal body.
        footer (list[HTMLElement]): Child elements within the modal footer.
        classes (list[str] | None): Additional CSS classes for the modal.
        id (str | None): Unique identifier for the modal.
        display_x (bool): Determines if the close button (X) is displayed.
    """

    def __init__(
        self,
        title: str | None = None,
        body: list[HTMLElement] | None = None,
        footer: list[HTMLElement] | None = None,
        closable: bool = True,
        classes: list[str] | None = None,
    ):
        """
        Initializes a `Modal` object with a title, body, footer, and optional CSS classes.

        Args:
            title (str | None): The modal's title (optional).
            body (list[HTMLElement] | None): Child elements for the modal body (default is an empty list).
            footer (list[HTMLElement] | None): Child elements for the modal footer (default is an empty list).
            closable (bool): Determines if the modal has a close button (default is True).
            classes (list[str] | None): Additional CSS classes for the modal (optional).

        Example:
            modal = Modal(
                title="My Modal",
                body=[Text("This is the modal body.")],
                footer=[Button("Close")]
            )
        """
        super().__init__(classes, "customModal")
        self.title = title
        self.body = body if body else []
        self.footer = footer if footer else []
        self.display_x = closable

    def add_body_element(self, element: HTMLElement):
        """
        Adds a child element to the modal body.

        Args:
            element (HTMLElement): The element to add to the modal body.

        Example:
            modal.add_body_element(Text("New body content"))
        """
        self.body.append(element)

    def add_footer_element(self, element: HTMLElement):
        """
        Adds a child element to the modal footer.

        Args:
            element (HTMLElement): The element to add to the modal footer.

        Example:
            modal.add_footer_element(Button("Save Changes"))
        """
        self.footer.append(element)

    def show(self):
        """
        Displays the modal window.

        Note:
            - Automatically assigns the modal an `id` of `customModal`.
            - Triggers the `showModal` task.
        """
        self.id = "customModal"
        add_task("", "showModal", content=self.construct())

    def hide(self):
        """
        Hides the modal window.

        Note:
            - Triggers the `hideModal` task to dynamically close the modal.
        """
        add_task("", "hideModal", content=self.construct())

    def construct(self) -> str:
        """
        Constructs the HTML for the modal.

        Returns:
            str: The HTML representation of the modal.

        Example:
            html = modal.construct()
            print(html)
        """
        header_html = (
            f'''
        <div class="modal-header">
            <h5 class="modal-title">{self.title}</h5>
            {'<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>' if self.display_x else ''}
        </div>
        '''
            if self.title
            else ""
        )

        body_html = "\n".join([child.construct() for child in self.body])
        footer_html = "\n".join([child.construct() for child in self.footer])
        classes_str = " ".join((self.classes or []) + ["modal", "fade"])
        id_attr = f'id="{self.id}"' if self.id else ""

        return f"""
        <div class="{classes_str}" {id_attr} tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    {header_html}
                    {f'<div class="modal-body">{body_html}</div>' if len(self.body) > 0 else ''}
                    {f'<div class="modal-footer">{footer_html}</div>' if len(self.footer) > 0 else ''}
                </div>
            </div>
        </div>
        """
