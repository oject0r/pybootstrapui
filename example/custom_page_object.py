from pybootstrapui import Page, components, templates

class MainPage(Page):
    def __init__(self):
        super().__init__(templates.Default)

        self.add(
            components.Header(components.BootstrapIcon('box-seam-fill'), 'Welcome to the Custom Page Object!'),
            components.Hr(),
            components.Text(
                'This example demonstrates how to create a custom page object using the PyBootstrapUI framework. '
                'By leveraging this framework, developers can efficiently build modern web interfaces with dynamic user interactions. '
                'The framework integrates seamlessly with Bootstrap components, enabling the rapid development of responsive and interactive web applications. '
                'Additionally, PyBootstrapUI supports the creation of desktop applications powered by NW.js, providing a versatile solution for both web and desktop environments.',
                font_size=15
            )
        )

if __name__ == '__main__':
    MainPage().run_in_desktop('/path/to/nwjs')
