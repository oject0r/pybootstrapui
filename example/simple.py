"""
Shows a simple Hello, world! Text on the screen.
"""

import pybootstrapui as ui
from pybootstrapui.components import *

page = ui.Page(ui.templates.Default)

page.add(
	Text('Hello, world!')
)

if __name__ == '__main__':
	page.run('/path/to/nwjs', title='Simple PyBootstrapUI Example')