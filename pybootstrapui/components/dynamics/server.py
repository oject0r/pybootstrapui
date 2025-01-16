from aiohttp import web
from .client_to_server import handle_action
from .queue_handler import fetch_task_results, get_tasks

# Инициализация приложения
app = web.Application()

# Глобальная переменная для страницы
app['pybsui_page'] = None

# Маршруты и обработчики
async def get_page(request):
    if app['pybsui_page'] is None:
        return web.Response(text="Page is not ready yet", status=503)  # Можно вернуть 503, если страница еще не готова
    html_content = await app['pybsui_page'].compile_async()
    return web.Response(text=html_content, content_type='text/html')

async def button_click(request):
    data = await request.json()
    response_data = await handle_action(data)
    return web.json_response(response_data)

async def get_content(request):
    return web.json_response(None)

async def _get_tasks(request):
    tasks = get_tasks()
    return web.json_response(tasks)

async def _task_result(request):
    data = await request.json()
    fetch_task_results(data)
    return web.Response(status=200)

# Добавляем маршруты в приложение
app.router.add_get('/', get_page)
app.router.add_post('/action', button_click)
app.router.add_get('/get_content', get_content)
app.router.add_get('/get_tasks', _get_tasks)
app.router.add_post('/task_result', _task_result)