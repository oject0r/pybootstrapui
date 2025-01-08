# Migrating to PyBootstrapUI 1.1.0  

The new version of **PyBootstrapUI** has been released!  

## 🚀 **How to Migrate?**  
You can explore updated examples in the **`example`** folder. Below are the key structural changes you need to be aware of:  

---

## 🟦 **Buttons**  

**Before:**  
```python
from pybootstrapui.components import Button
from pybootstrapui import ButtonCallbackContext

def button_callback(callback: ButtonCallbackContext):
    print(callback.id)

button = Button('Click Me', btn_style_type=ui.enums.ButtonStyle.PRIMARY, on_click=button_callback)
```

**Now:**  
```python
from pybootstrapui.components import Button, BootstrapIcon, ButtonStyle
from pybootstrapui import ButtonCallbackContext
import asyncio

async def button_callback(callback: ButtonCallbackContext):
    callback.show_spinner()
    await asyncio.sleep(15)
    print(callback.data, callback.id)
    callback.hide_spinner()

button = Button('Hello!', icon=BootstrapIcon('box-seam-fill'),
                style=ButtonStyle.PRIMARY, size=ButtonStyle.LARGE,
                on_click=button_callback, data='Button Data!')
```

**Changes:**  
- Added support for `async` callback functions.  
- Introduced spinner control via `show_spinner()` and `hide_spinner()`.  
- `btn_style_type` is now replaced with `style`.  
- Added `data` attribute for passing custom data to callbacks.  

---

## 🟩 **Inputs**  

**Before:**  
```python
from pybootstrapui.components import TextInput
from pybootstrapui import InputCallbackContext

def input_callback(context: ui.InputCallbackContext):
    print(f"Input value: {context.value}")

my_input = TextInput(label='Your Input', placeholder='Start typing...')
my_input.register_callbacks(on_input=input_callback)
```

**Now:**  
```python
from pybootstrapui.components import Input  # Same as TextInput
from pybootstrapui import InputCallbackContext

def input_callback(context: InputCallbackContext):
    print(context.value)

def on_enter_callback(context: InputCallbackContext):
    context.set_value('')

my_input = Input('Enter something',
                 on_input=input_callback,
                 on_enter=on_enter_callback)
```

**Changes:**  
- `TextInput` is as same as `Input`.  
- Callbacks are set directly as arguments (`on_input`, `on_enter`).  
- Added `on_enter` callback.  

---

## 🟧 **Whole HTML Elements**  

**Before:**  
```python
from pybootstrapui.components import Button

element = Button(unique_id='SuperUniqueID')
```

**Now:**  
```python
from pybootstrapui.components import Button

element = Button(id='SuperID')
```

**Changes:**  
- The `unique_id` parameter is now simply `id`.  

---

## 🟥 **Elements with Callbacks**  

Callbacks can now be assigned directly as attributes.  

**Before:**  
```python
my_input = TextInput(label='Your Input', placeholder='Start typing...')
my_input.register_callbacks(on_input=input_callback)
```

**Now:**  
```python
my_input = TextInput(label='Your Input', placeholder='Start typing...')
my_input.on_input = input_callback
```

**Changes:**  
- No need to call `.register_callbacks()`.  
- Callbacks can now be set directly as attributes.  

---

## 🟪 **Text Elements**  

Text elements now support more flexible configurations, including icons and colors.  

**Before:**  
```python
from pybootstrapui.components import Text, Header, BootstrapIcon

# You could only set icons for headers
Header('Hello, world', bi=BootstrapIcon('alphabet'))
Text('You can\'t set icons here ;(')
```

**Now:**  
```python
from pybootstrapui.components import Link, Text, Header, BootstrapIcon, RGBAColor

Header(BootstrapIcon('alphabet'), 'Hello, world!', BootstrapIcon('alphabet'))
Text(BootstrapIcon('archive-fill', color=RGBAColor(0, 0, 255, 0.4)), 'Wow, you can set icons!', color=RGBAColor(255, 0, 0))
Link(BootstrapIcon('archive-fill', color=RGBAColor(0, 0, 255, 0.4)), 'Here you can too!', color=RGBAColor(255, 0, 0))
```

**Changes:**  
- Icons can now be added to `Text` elements.  
- Icon and text parameters are passed via `*args`, while other settings are now `**kwargs`.  
- Color customization via `RGBAColor`.  

---

## ⚠️ **Reminder:**  
Double-check your application for errors after migration to ensure everything works correctly.  

Happy coding with **PyBootstrapUI 1.1.0**! 🚀✨  