from typing import Any
import asyncio
import uuid
import time


class QueueTask:
	def __init__(self, html_id: str, task_type: str):
		self.id = html_id
		self.type = task_type
		self.task_id = uuid.uuid4().hex
		self.result: QueueResult | None = None

	def wait(self):
		result = get_result(self)
		while not result:
			time.sleep(0.1)
			result = get_result(self)

		self.result = QueueResult(result, self.task_id)
		return self.result

	async def wait_async(self):
		result = get_result(self)
		while not result:
			await asyncio.sleep(0.1)
			result = get_result(self)

		self.result = QueueResult(result, self.task_id)
		return self.result


class QueueResult:
	def __init__(self, result: Any, task_id: str):
		self.task_id = task_id
		self.result = result

	def get(self):
		return self.result


class InvalidTaskException(Exception):
	def __init__(self, *args):
		super().__init__(args)

task_queue: list[QueueTask] = []
task_results = {}


def get_result(task: QueueTask) -> Any:
	if task.task_id not in task_results:
		return None

	result = task_results.pop(task.task_id)
	if task in task_queue:
		task_queue.remove(task)
	return result

def add_task(html_id: str, task_type: str, **kwargs):
	task = QueueTask(html_id, task_type)
	for key, value in kwargs.items():
		setattr(task, key, value)
	task_queue.append(task)
	return task