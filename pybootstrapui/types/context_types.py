from typing import Type, Any
from pybootstrapui.components.dynamics.queue import add_task


class CallbackContext:
    def __init__(self, id):
        """Init function."""
        self.id: str = id

    def from_dict(self, dictionary: dict[str, Any]):
        """From dict."""
        for key, value in dictionary.items():
            setattr(self, key, value)


class ButtonCallbackContext(CallbackContext):
    data: str

    def show_spinner(self):
        add_task(self.id, "showButtonSpinner")

    def hide_spinner(self):
        add_task(self.id, "hideButtonSpinner")


class InputCallbackContext(CallbackContext):
    value: str | int = ""

    def set_value(self, new_value):
        self.value = new_value
        add_task(self.id, 'setValue', value=new_value)



class ChoiceCallbackContext(CallbackContext):
    value: str = ""



class BlurCallbackContext(CallbackContext):
    pass


class FocusCallbackContext(CallbackContext):
    pass


class SliderCallbackContext(CallbackContext):
    value: int = 0

    def set_value(self, new_value: int):
        self.value = new_value
        add_task(self.id, 'setValue', value=new_value)


types: dict[str, Type[CallbackContext]] = {
    "button_click": ButtonCallbackContext,
    "on_input": InputCallbackContext,
    "on_enter": InputCallbackContext,
    "on_focus": FocusCallbackContext,
    "on_blur": BlurCallbackContext,
    "on_choice": ChoiceCallbackContext,
    "on_slider_change": SliderCallbackContext,
}
