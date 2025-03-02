from pybootstrapui import Page, components, modifiers
from pybootstrapui.desktop.built import NWJSPath


class MainPage(Page):

    CENTER_MODIFIER = modifiers.Modifier \
        .display(modifiers.DisplayValues.FLEX) \
        .justify_content(modifiers.JustifyContent.CENTER)

    def __init__(self):
        """Init function."""
        super().__init__()

        self.add(
            self.CENTER_MODIFIER.apply(
                components.Div( components.Header(
                    components.BootstrapIcon("box-seam-fill"), "Welcome to PyBootstrapUI"
                ) )
            ),
            components.HorizontalLine,
            components.Text(
                "This example demonstrates how to create a custom page object using the PyBootstrapUI framework. "
                "By leveraging this framework, developers can efficiently build modern web interfaces with dynamic user interactions. "
                "The framework integrates seamlessly with Bootstrap components, enabling the rapid development of responsive and interactive web applications. "
                "Additionally, PyBootstrapUI supports the creation of desktop applications powered by NW.js, providing a versatile solution for both web and desktop environments.",
                font_size=15,
            ),
        )


if __name__ == "__main__":
    page = MainPage()
    page.run_in_desktop(NWJSPath, title="Project Name — PyBootstrapUI")
