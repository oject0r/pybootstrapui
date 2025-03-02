from typing import Union, Callable, Awaitable
from . import add_handler
from .base import HasValue
from ..utils.callbacks import wrap_callback


class Slider(HasValue):
    """
    Represents a range slider component.

    Attributes:
        min (int): Minimum value of the slider.
        max (int): Maximum value of the slider.
        step (int): Increment step for the slider.
        value (int): Default value of the slider.
        label (str | None): Optional label displayed above the slider.
        show_value (bool): Whether to display the current value.
        callback (Callable | Awaitable | None): Function to execute when the slider value changes.
        classes (list[str] | None): Additional CSS classes for styling.
        id (str | None): Unique identifier for the slider.
    """

    def __init__(
        self,
        min: int = 0,
        max: int = 100,
        step: int = 1,
        value: int = 50,
        label: str | None = None,
        show_value: bool = True,
        on_slide: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes a `Slider` object.

        Args:
            min (int): Minimum value of the slider.
            max (int): Maximum value of the slider.
            step (int): Increment step for the slider.
            value (int): Default value of the slider.
            label (str | None): Optional label displayed above the slider.
            show_value (bool): Whether to display the current value.
            on_slide (Callable | Awaitable | None): Callback executed on value change.
            classes (list[str] | None): Additional CSS classes for styling.
            id (str | None): Unique identifier for the slider.

        Example:
            slider = Slider(
                min=0,
                max=100,
                step=5,
                value=50,
                label="Volume",
                show_value=True,
                callback=on_slider_change,
                classes=["custom-slider"]
            )
        """
        super().__init__(classes, id)
        self.min = min
        self.max = max
        self.step = step
        self.value = value
        self.label = label
        self.on_slide = on_slide
        self.show_value = show_value

    def construct(self) -> str:
        """
        Constructs the HTML and JavaScript representation of the slider.

        Returns:
            str: The HTML structure for the slider component.

        Example:
            html = slider.construct()
            print(html)
        """
        callback_js = (
            f"""
            sendEventCustom('{self.id}', 'on_slider_change', {{
                id: '{self.id}',
                value: this.value
            }});"""
            if self.on_slide
            else ""
        )

        if self.on_slide and self.id:
            add_handler("on_slider_change", self.id, wrap_callback(self.on_slide))

        return f"""
        <div class="slider-container {self.classes_str}">
            {f'<label for="{self.id}">{self.label}</label>' if self.label else ''}
            <input 
                type="range" 
                id="{self.id}" 
                min="{self.min}" 
                max="{self.max}" 
                step="{self.step}" 
                value="{self.value}" 
                class="form-range"
                oninput="document.getElementById('{self.id}-value').innerText = this.value; {callback_js}"
            >
            <span id="{self.id}-value" class="slider-value" {'style="display: none;"' if not self.show_value else ''}>{self.value}</span>
        </div>
        """
