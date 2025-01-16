import inspect
from typing import Callable
import pybootstrapui.types.context_types as ctx_types


handlers: dict[str, dict[str, Callable]] | dict[None, None] = {}


async def handle_action(data):
    event = data.get("event", "None")
    ddata = data.get("data", {})
    element_id = ddata.get("id", "unknown")

    await call_handler(event, element_id, ddata)

    return {"message": f"{element_id} got successfully!"}


def add_handler(handler_type: str, ctx_id: str, callback: Callable):
    global handlers
    """Add handler."""

    # Проверка на существование обработчика
    if handler_type not in handlers:
        handlers[handler_type] = {}

    # Добавляем обработчик
    handlers[handler_type][ctx_id] = callback


async def call_handler(event: str, ctx_id: str, data: dict):
    global handlers

    if event not in handlers:
        return

    if ctx_id not in handlers[event]:
        return

    handler = handlers[event][ctx_id]

    # Здесь можно отладить, что происходит с data_typed
    data_typed = ctx_types.types[event](ctx_id)
    data_typed.from_dict(data)

    if inspect.iscoroutinefunction(handler):
        await handler(data_typed)
    else:
        handler(data_typed)