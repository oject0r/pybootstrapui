# PyBootstrapUI

**PyBootstrapUI** is a Python framework for building modern web interfaces, integrating HTML components, dynamic user interactions, and creating desktop applications powered by **NW.js**.

---

## Key Features

- **Dynamic UI**: Build interactive web pages with server-side callbacks for user events.
- **Desktop Applications**: Launch web pages as standalone desktop apps using NW.js.
- **Prebuilt Components**: Access a library of ready-to-use HTML components like buttons, headers, forms, modals, and more.
- **Custom Templates**: Use predefined themes or your own HTML templates for quick styling.
- **Seamless Integration**: Works well with FastAPI and Bootstrap for modern web development.

---

## Quick Start

### Installation

1. Install the package:
   ```bash
   pip install pybootstrapui
   ```

2. Install **NW.js** if you plan to build desktop applications:
   - [Download NW.js](https://nwjs.io/).

---

### Basic Usage

#### Creating a Page

```python
from pybootstrapui import Page
from pybootstrapui.components import Header, Button
from pybootstrapui.templates import Default

# Create a new page
page = Page(template_filename=Default, page_title="Hello PyBootstrapUI")

# Add components
page.add(Header(label="Welcome to PyBootstrapUI!", header_size=1))
page.add(Button(label="Click Me", btn_style_type="primary"))

# Generate HTML
print(page.compile())
```

---

### Adding Callbacks

```python
from pybootstrapui import Page
from pybootstrapui.components import Header, Button
from pybootstrapui.templates import Default

# Define a callback function
def on_button_click(context):
    print(f"Button clicked with ID: {context.id}")

# Create a page with a button callback
page = Page(template_filename=Default, page_title="Callback Demo")
page.add(Header(label="Dynamic Callbacks Example"))
page.add(Button(label="Click Me", btn_style_type="primary", on_click=on_button_click))

# Run as a desktop application
page.run_in_desktop(
    nwjs_path="/path/to/nwjs",
    title="Callback App",
    width=800,
    height=600
)
```

---

## Running as a Desktop App

Use the `Page.run_in_desktop` method to run your page as a desktop application.

```python
from pybootstrapui import Page
from pybootstrapui.components import Header
from pybootstrapui.templates import Default

# Create the page
page = Page(template_filename=Default, page_title="My App")

# Add components
page.add(Header(label="This is a desktop app!"))

# Run the app
page.run_in_desktop(
    nwjs_path="/path/to/nwjs",
    icon="icon.png",
    title="My Desktop App",
    width=1024,
    height=768
)
```

---

## Documentation

Comprehensive documentation is available at [PyBootstrapUI Docs](https://pybootstrapui.076s.pw).

---

## Links

- **GitHub**: [oject0r/pybootstrapui](https://github.com/oject0r/pybootstrapui)
- **Documentation**: [pybootstrapui.076s.pw](https://pybootstrapui.076s.pw)
- **Bootstrap**: [getbootstrap.com](https://getbootstrap.com)
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
