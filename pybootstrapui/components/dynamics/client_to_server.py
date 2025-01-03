import inspect
from typing import Callable
from fastapi.responses import JSONResponse
import pybootstrapui.types.context_types as ctx_types
from .queue import add_task


handlers: dict[str, dict[str, Callable]] | dict[None, None] = {}


async def handle_action(data):
    event = data.get("event", "None")
    ddata = data.get("data", {})
    element_id = ddata.get("id", "unknown")
    await call_handler(event, element_id, ddata)
    return JSONResponse(content={"message": f"{element_id} got successfully!"})


def add_handler(handler_type: str, ctx_id: str, callback: Callable):
    if not handler_type in handlers:
        handlers[handler_type] = {}
    handlers[handler_type][ctx_id] = callback


async def call_handler(event: str, ctx_id: str, data: dict):
    if not event in handlers:
        handlers[event] = {}

    if ctx_id not in handlers[event].keys():
        return

    handler = handlers[event][ctx_id]

    data_typed = ctx_types.types[event](ctx_id)
    data_typed.from_dict(data)

    if event == "button_click" and data["indicateSpinner"]:
        add_task(ctx_id, "showButtonSpinner")

    if inspect.iscoroutinefunction(handler):
        await handler(data_typed)
    else:
        handler(data_typed)

    if event == "button_click" and data["indicateSpinner"]:
        add_task(ctx_id, "hideButtonSpinner")
