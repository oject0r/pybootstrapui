from typing import Union, Callable, Awaitable
from . import add_handler
from .base import HTMLElement, HasValue
from .text import Text
from ..utils import wrap_callback


# WIP

class Check(HasValue):
    def __init__(self, label: str | HTMLElement | None = None,
                 checked: bool = False,
                 changed: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
                 classes: list[str] | None = None,
                 id: str | None = None):
        super().__init__(classes, id)

        if isinstance(label, str):
            label = Text(label)

        self.label = label
        self.checked = checked
        self.changed = changed

    def change_value(self, new_value: bool):
        self.checked = new_value
        return super().change_value('true' if new_value else 'false')



    def construct(self) -> str:

        # Register the callback if provided
        if self.changed and self.id:
            add_handler("button_click", self.id, wrap_callback(self.changed))

        classes_str = ' ' + self.classes_str if self.classes else ''

        label_str = f'''
        <label class="form-check-label" for="{self.id}">
            {self.label}
        </label>
        ''' if self.label else ''

        return f'''
        <div class="form-check{classes_str}">
          <input class="form-check-input" type="checkbox" value="" id="{self.id}"{'checked' if self.checked else ''}>
          {label_str}
        </div>
        '''
