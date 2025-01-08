HOST = "127.0.0.1"
AJAX_PORT = 8000


def set_host(new):
    """Set host."""
    global HOST
    HOST = new


def set_port(new: int):
    """Set port."""
    global AJAX_PORT
    AJAX_PORT = new
