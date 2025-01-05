from .server import app
import pybootstrapui.components.dynamics.constants as constants
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)


def start_ajax_server(log_level="error"):
    """Запускает сервер FastAPI для AJAX."""
    import uvicorn

    uvicorn.run(app, host=constants.HOST, port=constants.AJAX_PORT, log_level=log_level)
