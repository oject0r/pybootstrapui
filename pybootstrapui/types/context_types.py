from typing import Type, Any

from pybootstrapui.components import add_task


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
    cursor_position: int = 0


class ChoiceCallbackContext(CallbackContext):
    value: str = ""


class BlurCallbackContext(CallbackContext):
    pass


class FocusCallbackContext(CallbackContext):
    pass


class SliderCallbackContext(CallbackContext):
    value: int = 0


types: dict[str, Type[CallbackContext]] = {
    "button_click": ButtonCallbackContext,
    "on_input": InputCallbackContext,
    "on_focus": FocusCallbackContext,
    "on_blur": BlurCallbackContext,
    "on_choice": ChoiceCallbackContext,
    "on_slider_change": SliderCallbackContext,
}
