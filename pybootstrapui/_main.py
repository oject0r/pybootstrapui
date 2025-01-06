import os
import random
import aiofiles
import rjsmin
import pybootstrapui.components
from pybootstrapui.components import add_task
from pybootstrapui.components.base import HTMLElement
from pybootstrapui.components.modals import Modal
from pybootstrapui.components.inputs import InputObject
from pybootstrapui.components.dynamics import start_ajax_server, constants
from pybootstrapui.desktop.nw_runner import run_page_in_desktop
import threading
import pybootstrapui.templates as templates
from pybootstrapui.components.dynamics import queue


with open(templates.InternalTemplates.JavaScript, "r", encoding="utf-8") as js_f:
    websocket_javascript = js_f.read()

with open(templates.InternalTemplates.GeneralStyle, "r", encoding="utf-8") as css_f:
    general_cascadingstyles = css_f.read()

custom_head_additions = f"""
<link href="https://vjs.zencdn.net/8.16.1/video-js.css" rel="stylesheet" /> <!-- Connect video.js -->
<style>{general_cascadingstyles}</style>
"""


class Page:
    """
    Represents a web page capable of managing content, navigation bar, and JavaScript inclusion.

    This class can compile and serve final HTML based on a template file and includes support
    for dynamic UI features via WebSockets.

    Attributes:
        path (os.PathLike | str | bytes): Path to the HTML template file.
        content (list[HTMLElement]): List of `HTMLElement` objects to include on the page.
        title (str | None): Title of the web page.
        javascript (str): JavaScript code included on the page.
        dynamic (bool): Whether to enable dynamic UI features.
        running (bool): Indicates if the page is actively running.
        inputs_saved_states (dict): Saved states of input elements.
        head (str): Custom HTML content added to the `<head>` section.
    """

    def __init__(
        self,
        template_filename: os.PathLike | str | bytes = templates.Default,
        content: list[HTMLElement] = None,
        page_title: str | None = None,
        dynamic_ui: bool = True,
        dynamic_ui_task_timing: int = 25,
    ):
        """
        Initializes a `Page` object.

        Args:
            template_filename (os.PathLike | str | bytes): Path to the HTML template file.
            content (list[HTMLElement], optional): List of `HTMLElement` objects to include on the page.
            page_title (str | None, optional): Title of the page.
            dynamic_ui (bool, optional): Whether to enable dynamic UI features. Default is `True`.
            dynamic_ui_task_timing (int, optional): Interval for client to check and complete tasks. Default is `25`.

        Example:
            page = Page(
                template_filename="path/to/template.html",
                content=[header, footer],
                page_title="My Page",
                dynamic_ui=True
            )

        Notes:
            - If `content` is not provided, it defaults to an empty list.
            - `dynamic_ui` determines if server callbacks and dynamic rendering are enabled.
        """
        self.path = template_filename
        self.content = content if content else []
        self.title = page_title
        self.dynamic = dynamic_ui
        self.dynamic_timing = dynamic_ui_task_timing
        self.running = False
        self.javascript = ""
        self.websocket_server = None
        self.inputs_saved_states = {}
        self.head = ""

    def add(self, *args):
        """
        Adds one or more elements to the page content.

        If the page is not running, the elements are added to `self.content`.
        If it is running, they are compiled into HTML and dynamically added to the frontend.

        Args:
            *args: One or more `HTMLElement` objects to add.

        Example:
            page.add(button, table, header)

        Notes:
            - If the page is already running, elements are dynamically rendered on the frontend.
        """
        if not self.running:
            [self.content.append(element) for element in args]
            return

        new_content = [element for element in args]
        compiled = "\n".join([element.construct() for element in new_content])

        queue.add_task("container", "addNew", content=compiled)

    def set_js(self, js_string: str):
        """
        Sets custom JavaScript code for the page.

        Args:
            js_string (str): JavaScript code to include on the page.

        Example:
            page.set_js("alert('Welcome to the page!');")

        Notes:
            - The provided JavaScript will be added as inline script content.
        """
        self.javascript = js_string

    def set_additional_head(self, html_string: str):
        """
        Adds custom HTML content to the `<head>` section of the template.

        Args:
            html_string (str): HTML code to include in the `<head>` section.

        Example:
            page.set_additional_head('<meta name="viewport" content="width=device-width, initial-scale=1">')

        Notes:
            - This only works if the template supports the `{custom_head}` placeholder.
        """
        self.head = html_string

    async def set_js_from_async(self, js_file: str | os.PathLike | bytes):
        """
        Asynchronously reads and sets JavaScript code from a file.

        Args:
            js_file (str | os.PathLike | bytes): Path to the JavaScript file.

        Raises:
            FileNotFoundError: If the file doesn't exist.

        Example:
            await page.set_js_from_async("path/to/script.js")

        Notes:
            - This method is useful for large or complex JavaScript files.
            - The JavaScript is automatically minified.
        """
        async with aiofiles.open(js_file, "r", encoding="utf-8") as f:
            self.javascript = await f.read()
            self.javascript = rjsmin.jsmin_for_posers(self.javascript)

    @staticmethod
    def show_spinner():
        """
        Shows a fullscreen spinner on the frontend.

        Example:
            Page.show_spinner()
        """
        add_task("", "showFullscreenSpinner")

    @staticmethod
    def hide_spinner():
        """
        Hides the fullscreen spinner on the frontend.

        Example:
            Page.hide_spinner()
        """
        add_task("", "hideFullscreenSpinner")


    async def reload(self):
        """
        Queues a task to reload the content of a specific container.

        This method compiles all the elements in `self.content`, constructs their HTML
        representation, and creates a `rewriteContent` task to update the frontend's
        container with the new content.

        Warning:
            - Frequent use is **not recommended**.
            - Prefer `HTMLElement.update()` for updates, especially when working with
              inputs and interactive elements.
            - This method may be deprecated in future versions.

        Example:
            await page.reload()

        Notes:
            - Assumes a container with the ID `container` exists in the frontend.
        """
        await self._save_input_states()
        compiled = []

        for element in self.content:
            if element.special_id in self.inputs_saved_states and isinstance(
                element, InputObject
            ):
                element.value = self.inputs_saved_states[element.special_id]

            compiled.append(element.construct())
        queue.add_task("container", "rewriteContent", newContent="\n".join(compiled))

    @staticmethod
    def run_js(javascript_code: str):
        """
        Queues a task to execute JavaScript code on the frontend.

        Args:
            javascript_code (str): JavaScript code to be executed.

        Example:
            Page.run_js("console.log('Hello, world!');")

        Notes:
            - Ensure the JavaScript code is valid and safe to execute.
            - Improper use might cause frontend errors or security risks.
        """
        queue.add_task("", "executeJavascript", code=javascript_code)

    def compile(self) -> str:
        """
        Compiles the page by reading the template file, replacing placeholders,
        and returning the final HTML.

        Returns:
            str: The compiled HTML content.

        Example:
            html = page.compile()
            print(html)
        """
        compiled = [element.construct() for element in self.content]
        compiled_string = (
            "\n".join(compiled)
            + '\n<script src="https://vjs.zencdn.net/8.16.1/video.min.js"></script>'
            + '\n<script src="https://cdnjs.cloudflare.com/ajax/libs/autosize.js/4.0.2/autosize.min.js"></script>'
        )

        with open(self.path, "r", encoding="utf-8") as f:
            content = f.read()

        self.javascript += (
            '</script>\n<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script><script>\n'
            + rjsmin.jsmin_for_posers(
                websocket_javascript.replace(
                    "!PYBSUI.INSERTHOST",
                    f"http://{constants.HOST}:{constants.AJAX_PORT}",
                ).replace("!PYBSUI.TASKTIMINGS", str(self.dynamic_timing))
            )
        )

        content = content.replace("{nav_content}", "")
        content = content.replace("{page_main}", compiled_string)
        content = content.replace("{page_name}", self.title if self.title else "")
        content = content.replace("{javascript_here}", self.javascript)
        content = content.replace("{custom_head}", self.head + custom_head_additions)
        return content

    async def compile_async(self) -> str:
        """
        Asynchronously compiles the page by reading the template file, replacing
        placeholders, and returning the final HTML.

        Returns:
            str: The compiled HTML content.

        Example:
            html = await page.compile_async()
            print(html)
        """
        compiled = [element.construct() for element in self.content]
        compiled_string = (
            "\n".join(compiled)
            + '\n<script src="https://vjs.zencdn.net/8.16.1/video.min.js"></script>'
        )

        async with aiofiles.open(self.path, "r", encoding="utf-8") as f:
            content = await f.read()

        self.javascript += (
            '</script>\n<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script><script>\n'
            + rjsmin.jsmin_for_posers(
                websocket_javascript.replace(
                    "!PYBSUI.INSERTHOST",
                    f"http://{constants.HOST}:{constants.AJAX_PORT}",
                )
            )
        )

        content = content.replace("{nav_content}", "")
        content = content.replace("{page_main}", compiled_string)
        content = content.replace("{page_name}", self.title if self.title else "")
        content = content.replace("{javascript_here}", self.javascript)
        content = content.replace("{custom_head}", self.head + custom_head_additions)

        return content

    async def _save_input_states(self):
        """
        Internal method to save the states of all `InputObject` instances on the page.

        Notes:
            - Uses `queue.add_task` to send commands to the frontend.
            - Stores states with keys corresponding to each input's `special_id`.

        Example:
            await page._save_input_states()
        """
        tasks = []
        ids = []
        for a in self.content:
            if not isinstance(a, InputObject):
                continue

            tasks.append(queue.add_task(a.id, "getValue"))
            ids.append(a.special_id)

        if not tasks:
            return

        await tasks[0].wait_async()

        for i, task in enumerate(tasks):
            self.inputs_saved_states[ids[i]] = task.result.get()

    def run_server(self):
        """
        Starts a local server for dynamic page updates.

        Notes:
            - Required for server-side interactions.
            - Runs in a separate thread.
        """
        self.running = True
        if self.dynamic:
            thread = threading.Thread(target=start_ajax_server, daemon=True)
            thread.start()

    async def clear(self):
        """
        Clears the content of the page.

        Example:
            await page.clear()
        """
        self.content = []
        task = queue.add_task("container", "rewriteContent", newContent="")
        await task.wait_async()
        return task.result.get()

    def run_in_desktop(
            self,
            nwjs_path: os.PathLike[str] | os.PathLike[bytes] | str | bytes,
            *,
            icon: os.PathLike[str] | os.PathLike[bytes] | str | bytes | None = None,
            title: str = "NW.js App",
            width: int = 800,
            height: int = 600,
            resizable: bool = True,
            server_bind: str = "127.0.0.1",
            server_port: int = 0,
    ):
        """
        Launches the page in NW.js as a desktop application.

        This method sets up and runs the application in NW.js runtime. It starts a local
        server for handling frontend interactions, configures server settings, and
        launches an NW.js desktop window.

        Args:
            nwjs_path (os.PathLike | str | bytes): Path to the NW.js executable.
            icon (os.PathLike | str | bytes | None, optional): Path to the application icon file.
            title (str, optional): Title of the application window. Defaults to `"NW.js App"`.
            width (int, optional): Width of the application window. Defaults to `800`.
            height (int, optional): Height of the application window. Defaults to `600`.
            resizable (bool, optional): Whether the application window is resizable. Defaults to `True`.
            server_bind (str, optional): IP address for the local server. Defaults to `"127.0.0.1"`.
            server_port (int, optional): Port number for the server. Defaults to a random port if `0`.

        Notes:
            - If `server_port` is `0`, a random port between `51000` and `65535` is selected.
            - Ensure `nwjs_path` points to a valid NW.js executable.
            - The server starts in a separate thread for handling dynamic interactions.

        Example:
            ```python
            page.run_in_desktop(
                nwjs_path="path/to/nwjs",
                icon="path/to/icon.png",
                title="My Desktop App",
                width=1024,
                height=768,
                resizable=False,
                server_bind="localhost",
                server_port=52000
            )
            ```
        """
        if server_port == 0:
            server_port = random.randint(51000, 65535)

        if isinstance(nwjs_path, bytes):
            nwjs_path = nwjs_path.decode("utf-8")

        constants.set_host(server_bind)
        constants.set_port(server_port)
        self.run_server()
        run_page_in_desktop(self, str(nwjs_path), icon, title, width, height, resizable)

