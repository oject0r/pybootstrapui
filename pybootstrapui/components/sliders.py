from typing import Union, Callable, Awaitable
from . import add_handler
from .base import HTMLElement
from pybootstrapui.components.dynamics.queue import add_task
from ..utils.callbacks import wrap_callback


class Slider(HTMLElement):
    """
    A class representing a range slider component.

    Attributes:
            - min (int): Minimum value of the slider.
            - max (int): Maximum value of the slider.
            - step (int): Increment step for the slider.
            - value (int): Default value of the slider.
            - label (str | None): Optional label for the slider.
            - callback (Callable | None): Function called on value change.
            - classes (list[str] | None): Additional CSS classes.
            - unique_id (str | None): Unique identifier.
    """

    def __init__(
        self,
        min: int = 0,
        max: int = 100,
        step: int = 1,
        value: int = 50,
        label: str | None = None,
        show_value: bool = True,
        callback: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """
        Initializes a slider component.

        Parameters:
                - min (int): Minimum value of the slider.
                - max (int): Maximum value of the slider.
                - step (int): Increment step.
                - value (int): Default value of the slider.
                - label (str | None): Optional label displayed above the slider.
                - callback (Callable | None): Function to be executed when the slider value changes.
                - classes (list[str] | None): Additional CSS classes for styling the slider.
                - unique_id (str | None): Unique identifier for the slider element.

        Notes:
                - If callback is provided, it will be executed every time the slider value changes.
                - The unique_id is required for identifying slider events on the frontend.
        """
        super().__init__(classes, unique_id)
        self.min = min
        self.max = max
        self.step = step
        self.value = value
        self.label = label
        self.callback = callback
        self.show_value = show_value

        # Register the callback if provided
        if callback and self.id:
            add_handler("on_slider_change", self.id, wrap_callback(callback))

    def construct(self) -> str:
        """
        Constructs the HTML and JavaScript representation of the slider.

        Returns:
                - str: Combined HTML and JavaScript as a string.

        HTML Structure:
        - A div container wraps the slider, an optional label, and the displayed value.
        - The slider is created using an <input> of type range.
        - A <span> element displays the current value dynamically.

        JavaScript Behavior:
        - The oninput event updates the displayed value in real-time.
        - If a callback is set, an event is triggered on the server-side with the new value.

        Example Output:
        html
        <div class="slider-container">
                <label for="slider-id">Volume</label>
                <input
                        type="range"
                        id="slider-id"
                        min="0"
                        max="100"
                        step="1"
                        value="50"
                        oninput="document.getElementById('slider-id-value').innerText = this.value; sendEventCustom('slider-id', 'on_slider_change', {id: 'slider-id', value: this.value});"
                >
                <span id="slider-id-value">50</span>
        </div>
        
        """
        callback_js = (
            f"""
            sendEventCustom('{self.id}', 'on_slider_change', {{
            	id: '{self.id}',
                value: this.value
            }});
        """
            if self.callback
            else ""
        )

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

    def set_value(self, new_value: int):
        """
        Sets the slider's value dynamically.

        Parameters:
                - new_value (int): The new value to set for the slider.

        Notes:
                - The value is updated both on the frontend and server-side.
                - The value is clamped between min and max.

        Example:
                python
                slider.set_value(75)
                
        """
        self.value = max(self.min, min(new_value, self.max))
        add_task(self.id, "setValue", value=new_value)
        add_task(
            f"{self.id}-value",
            "rewriteContent",
            newContent=str(new_value),
            transitionTime=0,
        )

    async def get_value(self) -> int:
        """
        Asynchronously retrieves the current value of the slider.

        Returns:
                - int: The current value of the slider.

        Notes:
                - This method queues a task to fetch the slider's value dynamically from the frontend.
                - If the value cannot be fetched, it will return the last known value.

        Example:
                python
                current_value = await slider.get_value()
                print(f"Slider value: {current_value}")
                
        """
        task = add_task(self.id, "getValue")
        await task.wait_async()
        return task.result.result.get("value", self.value)
