from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .client_to_server import handle_action
from .queue_handler import fetch_task_results, get_tasks

app = FastAPI()


@app.post("/action")
async def button_click(request: Request):
    return await handle_action(await request.json())


@app.get("/get_content")
async def get_content():
    return None


@app.get("/get_tasks")
async def _get_tasks():
    return JSONResponse(content=get_tasks())


@app.post("/task_result")
async def _task_result(request: Request):
    data = await request.json()
    fetch_task_results(data)
