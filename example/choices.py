"""
Demonstrates a choice component with multiple selectable options.
"""

import pybootstrapui as ui
from pybootstrapui.components import *

page = ui.Page(ui.templates.Default)

def choice_callback(context: ui.ChoiceCallbackContext):
    print(f"Selected choice: {context.value}")

page.add(
    Text('Pick an option below:'),
    Choice(options=[Option('Option 1', value='option_1'), Option('Option 2', value='option_2'), Option('Option 3', value='option_3')], on_choice=choice_callback)
)

if __name__ == '__main__':
    page.run_in_desktop('/path/to/nwjs', title='Choice Example')
