from pybootstrapui import Page, ButtonCallbackContext
from pybootstrapui import templates
from pybootstrapui.components import *
import aiohttp  # not used in requirements, install yourself

page = Page(templates.Default)

webhook_input = InputObject('Enter Webhook URL', 'url')
content_input = TextArea('Enter Message Content')

async def send_webhook(ctx: ButtonCallbackContext):
	async with aiohttp.ClientSession() as session:
		webhook_url = await webhook_input.get_value()
		message_content = await content_input.get_value()
		await session.post(webhook_url, data={'content': message_content})

send_button = Button('Send', callback=send_webhook)

page.add(
	Card([webhook_input, content_input, send_button])
)

if __name__ == '__main__':
	page.run_in_desktop('D:\\nwjs\\nw.exe', title='Discord Webhook Sender')