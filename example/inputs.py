"""
Shows an input field that logs the entered value on change.
"""

import pybootstrapui as ui
from pybootstrapui.components import *

page = ui.Page(ui.templates.Default)

def input_callback(context: ui.InputCallbackContext):
    print(f"Input value: {context.value}")

my_input = Input(label='Your Input', placeholder='Start typing...')
my_input.on_input = input_callback

page.add(
    Text('Type something below:'),
    my_input
)

if __name__ == '__main__':
    page.run('/path/to/nwjs', title='Input Example')
