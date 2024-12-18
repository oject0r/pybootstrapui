from pybootstrapui.mishmash import Page, Default, ButtonStyle, ButtonCallbackContext, Spacing, Position
import pybootstrapui.components as components

page = Page(Default)

header_1 = components.Header('PyBootstrapUI', bi=components.BootstrapIcon('box-seam-fill'))

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
	page.add(components.Text('Hello!', classes=[Spacing.MARGIN_TOP_2]))

page.add(
	header_1,
	components.Text('This file is made to show dynamic additions to pages.'),
	components.Button('Click me!', btn_style_type=ButtonStyle.SUCCESS, callback=add_new_callback, classes=['bottom-left-corner'])
)

if __name__ == '__main__':
	page.run_in_desktop('D:\\nwjs-debug\\nw.exe')