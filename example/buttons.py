"""
Demonstrates a button with a click event.
"""

import pybootstrapui as ui
from pybootstrapui.components import *

page = ui.Page(ui.templates.Default)

def button_callback(context: ui.ButtonCallbackContext):
    print("Button clicked!")

page.add(
    Text('Press the button below:'),
    Button('Click Me', btn_style_type=ui.enums.ButtonStyle.PRIMARY, on_click=button_callback)
)

if __name__ == '__main__':
    page.run_in_desktop('D:\\nwjs\\nw.exe', title='Button Example')
