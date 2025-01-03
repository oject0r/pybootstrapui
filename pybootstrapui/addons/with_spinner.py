from functools import wraps
from pybootstrapui.components import add_task


def with_spinner_indicator(func):
    """
    Decorator to display a fullscreen spinner indicator during the execution of an asynchronous function.

    This decorator adds a task to show a fullscreen spinner before the function starts
    and hides it after the function completes.

    Args:
            func (Callable): An asynchronous function to be wrapped.

    Returns:
            Callable: The wrapped asynchronous function with spinner management.

    Example:
            @with_spinner_indicator
            async def fetch_data():
                    await some_async_operation()
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        add_task("", "showFullscreenSpinner")
        try:
            result = await func(*args, **kwargs)
        finally:
            add_task("", "hideFullscreenSpinner")
        return result

    return wrapper
