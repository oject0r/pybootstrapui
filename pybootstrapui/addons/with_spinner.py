from functools import wraps
from pybootstrapui.components import add_task
import asyncio
from typing import Callable, Any


def with_spinner_indicator(func: Callable) -> Callable:
    """
    Decorator to display a fullscreen spinner indicator during the execution of a function.

    This decorator adds a task to show a fullscreen spinner before the function starts
    and hides it after the function completes, regardless of success or failure.

    Parameters:
        func (Callable): An asynchronous or synchronous function to be wrapped.

    Returns:
        Callable: The wrapped function with spinner management.

    Example:
        @with_spinner_indicator
        async def fetch_data():
            await some_async_operation()
    """
    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        add_task("", "showFullscreenSpinner")
        try:
            return await func(*args, **kwargs)
        finally:
            add_task("", "hideFullscreenSpinner")

    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        add_task("", "showFullscreenSpinner")
        try:
            return func(*args, **kwargs)
        finally:
            add_task("", "hideFullscreenSpinner")

    # Determine if the function is async or sync
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper