import asyncio

def wrap_callback(callback):
	"""
	Wraps the callback to handle synchronous and asynchronous functions.

	Parameters:
		callback (Callable): The original callback function.

	Returns:
		Callable: A wrapped callback that can handle WebSocket events.
	"""

	async def wrapped(data):
		if asyncio.iscoroutinefunction(callback):
			await callback(data)
		else:
			callback(data)

	return wrapped