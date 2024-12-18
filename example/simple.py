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
	page.run_in_desktop('D:\\nwjs\\nw.exe', title='Simple PyBootstrapUI Example')