"""
Displays a table with headers and rows of data.
"""

import pybootstrapui as ui
from pybootstrapui.components import *

page = ui.Page(ui.templates.Default)

page.add(
    Text('Table example:'),
    Table(headers=['ID', 'Name', 'Email'], rows=[[1, 'John Doe', 'john@example.com'], [2, 'Jane Smith', 'jane@example.com']])
)

if __name__ == '__main__':
    page.run_in_desktop('/path/to/nwjs', title='Table Example')
