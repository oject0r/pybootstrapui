from aiohttp import web
import asyncio
from .client_to_server import handle_action
from .queue_handler import fetch_task_results, get_tasks

app = web.Application()

app['pybsui_page'] = None

async def get_page(request):
    if app['pybsui_page'] is not None:
        return web.Response(text=await app['pybsui_page'].compile_async(), content_type='text/html')
    else:
        return web.Response(text="Page not found", status=404)

async def button_click(request):
    data = await request.json()
    result = await handle_action(data)
    return web.json_response(result)

async def get_content(request):
    # Здесь можно вернуть нужный контент
    return web.json_response(None)

async def _get_tasks(request):
    tasks = get_tasks()
    return web.json_response(tasks)

async def _task_result(request):
    data = await request.json()
    fetch_task_results(data)
    return web.Response(text="Task result received", status=200)

app.router.add_get('/', get_page)
app.router.add_post('/action', button_click)
app.router.add_get('/get_content', get_content)
app.router.add_get('/get_tasks', _get_tasks)
app.router.add_post('/task_result', _task_result)

if __name__ == '__main__':
    web.run_app(app)