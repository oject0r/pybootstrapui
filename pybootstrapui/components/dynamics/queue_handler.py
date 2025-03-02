from pybootstrapui.components.dynamics.queue import task_queue, task_results
from typing import Any, Union


def fetch_task_results(data: dict[str, Any]):
    """Updates task results with data from the
    client.

    Parameters:
            data (dict[str, Any]): A dictionary where keys are task IDs (html_id) and values are results.

    Notes:
            - Ensures that only valid task IDs are updated in task_results.
            - Ignores any invalid or unexpected entries in the input data.
    """
    if not isinstance(data, dict):
        return

    task_results[data["task_id"]] = data["result"]


def get_tasks() -> dict[str, dict[str, Union[int, str, dict]]]:
    """Get tasks."""
    tasks = {}
    for task in task_queue:
        task_data = {
            "id": task.id,
            "type": task.type,
        }

        additional_attrs = {
            key: value
            for key, value in vars(task).items()
            if key not in {"id", "type", "task_id", "result"}
        }

        task_data.update(additional_attrs)
        tasks[task.task_id] = task_data

    task_queue.clear()
    return tasks
