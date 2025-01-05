"""
Unimport this if you imported that directly.
"""

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
    A class representing a web page, capable of managing content, navigation bar,
    and JavaScript inclusion. It can compile and serve the final HTML based on a template file.

    Attributes:
            - path (os.PathLike | str | bytes): The file path to the HTML template.
            - content (list[HTMLElement]): A list of HTMLElement objects to be included in the page.
            - title (str | None): The title of the page (optional).
            - javascript (str): A string containing JavaScript code to be included in the page (default is empty).
            - dynamic (bool): Indicates if the page should use Dynamic UI features (e.g., WebSocket server for callbacks).
            - running (bool): A flag indicating if the page is actively running.
            - inputs_saved_states (dict): Stores the saved states of input elements on the page.
            - head (str): Custom HTML content to include in the <head> section of the template.
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
        Initializes a Page object.

        Parameters:
                - template_filename (os.PathLike | str | bytes): The file path to the HTML template.
                - content (list[HTMLElement]): A list of HTMLElement objects to be included in the page (optional).
                - page_title (str | None): The title of the page (optional).
                - dynamic_ui (bool): Specifies whether Dynamic UI features should be enabled, such as WebSocket support.
                - dynamic_ui_task_timing (int): How fast client is going to check for new tasks and complete them.

        Example:
                # Create a page with a template and title
                
                page = Page(
                        template_filename="path/to/template.html",
                        content=[header, footer],
                        page_title="My Page",
                        dynamic_ui=True
                )
                

        Note:
                - If content is not provided, it defaults to an empty list.
                - The dynamic_ui flag determines if callbacks and server-based interactions are enabled.
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
        Adds an element (or a list of elements) to the content of the page.

        This method appends new elements to the page's self.content list if the page
        is not currently running. If the page is running, the new elements are compiled
        into HTML and dynamically added to the frontend.

        Parameters:
                - *args: One or more elements to add to the page's content.

        Example:
                # Add elements to the page
                
                page.add(button, table, header)
                

        Note:
                - If the page is running, the elements are directly sent to the frontend for
                  dynamic rendering.
        """
        if not self.running:
            [self.content.append(element) for element in args]
            return

        new_content = [element for element in args]
        compiled = "\n".join([element.construct() for element in new_content])

        queue.add_task("container", "addNew", content=compiled)

    def set_js(self, js_string: str):
        """
        Sets the JavaScript code for the page from a string.

        Parameters:
                - js_string (str): The JavaScript code to include in the page.

        Example:
                # Add custom JavaScript to the page
                
                page.set_js("alert('Welcome to the page!');")
                

        Note:
                - The provided JavaScript will be used as the page's custom script.
        """
        self.javascript = js_string

    def set_additional_head(self, html_string: str):
        """
        Adds custom HTML code to the <head> section of the template.

        If the page's template includes a {custom_head} placeholder, this method
        allows for injecting custom HTML content into that section.

        Parameters:
                - html_string (str): The HTML code to inject into the page's <head>.

        Example:
                # Add meta tags to the page
                
                page.set_additional_head('<meta name="viewport" content="width=device-width, initial-scale=1">')
                

        Note:
                - This method is only effective if the template supports custom <head> content.
        """
        self.head = html_string

    async def set_js_from_async(self, js_file: str | os.PathLike | bytes):
        """
        Asynchronously reads and sets the JavaScript code for the page from a file.

        This method reads the contents of the provided JavaScript file, minifies it
        using rjsmin.jsmin_for_posers, and sets it as the page's custom script.

        Parameters:
                - js_file (str | os.PathLike | bytes): The path to the JavaScript file.

        Example:
                # Load and set JavaScript from a file
                
                await page.set_js_from_async("path/to/script.js")
                

        Note:
                - The file must be UTF-8 encoded for proper reading.
                - This method is ideal for including large or complex JavaScript files dynamically.
        """
        async with aiofiles.open(js_file, "r", encoding="utf-8") as f:
            self.javascript = await f.read()
            self.javascript = rjsmin.jsmin_for_posers(self.javascript)

    @staticmethod
    def show_spinner():
        add_task("", "showFullscreenSpinner")

    @staticmethod
    def hide_spinner():
        add_task("", "hideFullscreenSpinner")

    async def reload(self):
        """
        Warning:
                # Not recommended to use much.

                # Better use HTMLElement.update() ESPECIALLY if you have inputs and page updates on their change.

                # Still useful in some cases, so this method is still here.

                # Going to become deprecated in future versions.

        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        Queues a task to reload the content of a specific container.

        This method compiles all the elements in the self.content list,
        constructs their HTML representation, and creates a rewriteContent
        task to update the frontend's container with the new content.

        Tasks are added to the task queue for asynchronous execution.

        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        Example:
                # Reload the container with updated content

                await page.reload()

        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        Note:

                This assumes a container with the ID 'container' exists in the frontend.

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
    def run_js(javascript_code):
        """
        Queues a task to execute custom JavaScript code on the frontend.

        This method creates an executeJavascript task in the task queue
        to execute the provided JavaScript code asynchronously in the browser.

        Parameters:
                - javascript_code (str): The JavaScript code to be executed.

        Example:
                # Run custom JavaScript on the frontend
                Page.run_js("console.log('Hello, world!');")

        Note:
                - Ensure the provided JavaScript code is safe to execute and
                  valid for the frontend environment.
                - This is useful for adding dynamic behaviors or debugging,
                  but improper use could lead to frontend errors or security issues.
        """
        queue.add_task("", "executeJavascript", code=javascript_code)

    def compile(self):
        """
        Compiles the page by reading the template file, replacing placeholders, and returning the final HTML.

        Returns:
                str: The compiled HTML content.
        """
        compiled = [element.construct() for element in self.content]
        compiled_string = (
            "\n".join(compiled)
            + '\n<script src="https://vjs.zencdn.net/8.16.1/video.min.js"></script>'
        )
        navbar_compiled = ""

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

    async def compile_async(self):
        """
        Asynchronously compiles the page by reading the template file, replacing placeholders, and returning the final HTML.

        Returns:
                str: The compiled HTML content.
        """
        compiled = [element.construct() for element in self.content]
        compiled_string = (
            "\n".join(compiled)
            + '\n<script src="https://vjs.zencdn.net/8.16.1/video.min.js"></script>'
        )
        navbar_compiled = ""

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

        content = content.replace("{nav_content}", navbar_compiled)
        content = content.replace("{page_main}", compiled_string)
        content = content.replace("{page_name}", self.title)
        content = content.replace("{javascript_here}", self.javascript)
        content = content.replace("{custom_head}", self.head + custom_head_additions)

        return content

    async def _save_input_states(self):
        """
        Warning:
                # Internal method, not intended for direct use.

                # Handles saving the state of input elements on the page.

        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        Collects the current states of all InputObject instances in self.content,
        requesting their values asynchronously and saving them in self.inputs_saved_states.

        This method uses a task queue to ensure asynchronous execution and
        collects results into a local dictionary.

        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        Note:
                - Relies on queue.add_task to send commands to the frontend.
                - Only works if InputObject instances are properly added to self.content.
                - Results are stored with keys corresponding to each input's special_id.

        Example:
                # Save input states for later restoration
                await page._save_input_states()

        """
        tasks = []
        ids = []
        for a in self.content:
            if not isinstance(a, InputObject):
                continue

            tasks.append(queue.add_task(a.id, "getValue"))
            ids.append(a.special_id)
        if not len(tasks) > 0:
            return
        await tasks[0].wait_async()

        for i, task in enumerate(tasks):
            self.inputs_saved_states[ids[i]] = task.result.get()

    def run_server(self):
        """
        Starts a local server for dynamic page updates.

        If the page is marked as dynamic (self.dynamic is True),
        this method creates a separate thread to handle AJAX requests
        using start_ajax_server.

        Note:
                - This is essential for server-side interaction with the frontend.
                - Designed to work asynchronously with other parts of the framework.

        """
        self.running = True
        if self.dynamic:
            thread = threading.Thread(target=start_ajax_server, daemon=True)
            thread.start()

    async def clear(self):
        """
        Clears the content of the page.

        This method resets the self.content list to an empty state and sends a task
        to the frontend to clear the container's content dynamically.

        Example:
                # Clear all elements from the page
                await page.clear()
        """
        self.content = []
        task = queue.add_task("container", "rewriteContent", newContent="")
        await task.wait_async()
        return task.result.get()

    def get_element_by_id(self, element_id: str) -> HTMLElement | None:
        """
        Retrieves an element from the page by its unique ID.

        Parameters:
                - element_id (str): The ID of the element to retrieve.

        Returns:
                - HTMLElement | None: The element with the specified ID, or None if not found.

        Example:
                # Get an element by ID
                element = page.get_element_by_id('button1')
        """
        for element in self.content:
            if element.id == element_id:
                return element
        return None

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

        This method configures and starts the application as a desktop app
        using the NW.js runtime. It binds the server to the specified address and port,
        starts a local server in the background, and launches the app window.

        Parameters:
                - nwjs_path (str | bytes): Path to the NW.js executable.
                - icon (str | bytes | None): Optional path to the window icon file.
                - title (str): Title of the application window.
                - width (int): Width of the application window (default: 800).
                - height (int): Height of the application window (default: 600).
                - resizable (bool): Whether the application window is resizable (default: True).
                - server_bind (str): IP address to bind the local server (default: '127.0.0.1').
                - server_port (int): Port number for the local server (default: random port if 0).

        Note:
                - If server_port is not specified, a random port between 51000 and 65535 is chosen.
                - Calls run_page_in_desktop with the appropriate arguments after configuring the server.

        Example:
                # Run the page as a desktop application with NW.js
                
                page.run_in_desktop(
                        nwjs_path="path/to/nwjs",
                        icon="path/to/icon.png",
                        title="My App",
                        width=1024,
                        height=768,
                        resizable=False
                )
                

        """
        if server_port == 0:
            server_port = random.randint(51000, 65535)

        if isinstance(nwjs_path, bytes):
            nwjs_path = nwjs_path.decode("utf-8")

        constants.set_host(server_bind)
        constants.set_port(server_port)
        self.run_server()
        run_page_in_desktop(self, str(nwjs_path), icon, title, width, height, resizable)
