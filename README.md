# PyBootstrapUI

**PyBootstrapUI** is a Python framework for building modern web interfaces, integrating HTML components, dynamic user interactions, and creating desktop applications powered by **NW.js**.

---

## 🚀 **Key Features**

- **🖥️ Dynamic UI:** Build interactive web pages with server-side callbacks for user events.
- **💻 Desktop Applications:** Launch web pages as standalone desktop apps using NW.js.
- **📦 Prebuilt Components:** Access a library of ready-to-use HTML components like buttons, headers, forms, modals, and more.
- **🎨 Custom Templates:** Use predefined themes or your own HTML templates for quick styling.
- **🔗 Seamless Integration:** Works well with FastAPI and Bootstrap for modern web development.

---

## ⚡ **Quick Start**

### 📥 **Installation**

1. Install the package:
   ```bash
   pip install pybootstrapui
   ```

2. Install **NW.js** if you plan to build desktop applications:
   - [Download NW.js](https://nwjs.io/).
   - Or use the PyBootstrapUI command:
     ```bash
     python -m pybootstrapui download %path_to_nwjs%
     ```

---

### 📝 **Basic Usage**

#### **📄 Creating a Page**

```python
from pybootstrapui import Page
from pybootstrapui.components import Header, Button, ButtonStyle, BootstrapIcon

# Create a new page
page = Page(page_title="Hello PyBootstrapUI")

# Add components
page.add(Header(BootstrapIcon('box-seam-fill'), "Welcome to PyBootstrapUI!"))
page.add(Button(label="Click Me", style=ButtonStyle.PRIMARY))

# Generate HTML
print(page.compile())
```

---

#### **🔄 Adding Callbacks**

```python
import asyncio
from pybootstrapui import Page, ButtonCallbackContext
from pybootstrapui.components import Header, Button, ButtonStyle
from pybootstrapui.templates import Default


# Define a callback function
async def on_button_click(context: ButtonCallbackContext):
    context.show_spinner()
    
    print(f"Button clicked with ID: {context.id}")
    await asyncio.sleep(15)
    
    context.hide_spinner()


# Create a page with a button callback
page = Page(template_filename=Default, page_title="Callback Demo")
page.add(Header("Dynamic Callbacks Example"))
page.add(Button("Click Me", style=ButtonStyle.SUCCESS_OUTLINE, on_click=on_button_click))

# Run as a desktop application
page.run_in_desktop(
    nwjs_path="/path/to/nwjs",
    title="Callback App",
    width=800,
    height=600
)
```

---

## 🖥️ **Running as a Desktop App**

Use the `Page.run_in_desktop` method to run your page as a desktop application.

```python
from pybootstrapui import Page
from pybootstrapui.components import Header

# Create the page
page = Page(page_title="My App")

# Add components
page.add(Header("This is a desktop app!"))

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

## 📦 **Easy Packaging**

Easily package and distribute your **PyBootstrapUI** applications with minimal effort!

### 🛠️ **Step 1: Create a New Project**

Generate a fully templated **PyBootstrapUI** project structure:

```bash
python -m pybootstrapui create MyProject
```

### ⚙️ **Step 2: Build Your Application**

Package your application into a standalone build:

```bash
python -m pybootstrapui build MyProject
```

- **Dependencies Management:** All required packages are bundled.
- **Optimized Build Process:** Ensures efficient and clean packaging.
- **Platform-Specific Binaries:** Create executables for Windows, macOS, or Linux seamlessly.

---

## 📚 **Documentation**

Detailed documentation is available at [PyBootstrapUI Docs](https://pybootstrapui.076s.pw) (WIP).

---

## 🔗 **Useful Links**

- **GitHub:** [oject0r/pybootstrapui](https://github.com/oject0r/pybootstrapui)
- **Documentation:** [pybootstrapui.076s.pw](https://pybootstrapui.076s.pw)
- **Bootstrap:** [getbootstrap.com](https://getbootstrap.com)
- **FastAPI:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

## 📜 **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

✨ Start building beautiful, dynamic, and cross-platform applications with **PyBootstrapUI** today! 🚀

