import pybootstrapui.components as components
from pybootstrapui import Page, ButtonCallbackContext
from pybootstrapui.templates import Default
from pybootstrapui.modifiers import *

page = Page(Default)

header_1 = components.Header(components.BootstrapIcon('box-seam-fill'), 'PyBootstrapUI')

page.set_additional_head('''
<style>
	.bottom-left-corner {
	    position: fixed;
        bottom: 20px;
    	left: 20px;
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
	}
</style>
''')

def add_new_callback(context: ButtonCallbackContext):
	page.add(components.Text('Hello!'))

page.add(
	header_1,
	components.Text('This file is made to show dynamic additions to pages.'),
	components.Button('Click me!', modifier=ButtonModifier.color(ButtonStyle.SUCCESS), on_click=add_new_callback, classes=['bottom-left-corner'])
)

if __name__ == '__main__':
	page.run('/path/to/nwjs', title='Dynamic Example')