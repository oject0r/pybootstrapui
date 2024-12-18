"""
Displays formatted Markdown text.
"""

import pybootstrapui as ui
from pybootstrapui.components import *

page = ui.Page(ui.templates.Default)

page.add(
    Text('Markdown example:'),
    Markdown('# Hello Markdown\nThis is an example of Markdown in PyBootstrapUI.')
)

if __name__ == '__main__':
    page.run_in_desktop('D:\\nwjs\\nw.exe', title='Markdown Example')
