from .server import app
import pybootstrapui.components.dynamics.constants as constants
from aiohttp import web
import logging


async def init_pybsui_page(app, page):
    app['pybsui_page'] = page


def start_ajax_server(page):
    logging.getLogger('aiohttp.access').setLevel(logging.ERROR)
    logging.getLogger('aiohttp.server').setLevel(logging.ERROR)
    logging.getLogger('aiohttp.web').setLevel(logging.ERROR)
    logging.getLogger('aiohttp.client').setLevel(logging.ERROR)

    app.on_startup.append(lambda app: init_pybsui_page(app, page))
    web.run_app(app, host=constants.HOST, port=constants.AJAX_PORT)
