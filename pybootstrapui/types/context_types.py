from typing import Type, Any


class CallbackContext:
    def __init__(self, id):
        self.id: str = id

    def from_dict(self, dictionary: dict[str, Any]):
        for key, value in dictionary.items():
            setattr(self, key, value)


class ButtonCallbackContext(CallbackContext):
    data: str


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
