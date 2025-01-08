import asyncio


def wrap_callback(callback):
    """Wraps the callback to handle synchronous
    and asynchronous functions.
    """

    async def wrapped(data):
        if asyncio.iscoroutinefunction(callback):
            await callback(data)
        else:
            callback(data)

    return wrapped
