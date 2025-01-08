"""
Demonstrates a button with a click event.
"""

import pybootstrapui as ui
from pybootstrapui.components import *
import asyncio


page = ui.Page(ui.templates.Default)

async def button_callback(context: ui.ButtonCallbackContext):
    context.show_spinner()
    await asyncio.sleep(15)
    context.hide_spinner()

page.add(
    Text('Press the button below:'),
    Button('Click Me', style=ui.enums.ButtonStyle.PRIMARY, on_click=button_callback)
)

if __name__ == '__main__':
    page.run_in_desktop('/path/to/nwjs', title='Button Example')
