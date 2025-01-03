"""
A simple currency converter using an external API.
"""

from pybootstrapui import Page, ButtonCallbackContext
from pybootstrapui import templates
from pybootstrapui.components import *
import aiohttp

page = Page(templates.Default)

amount_input = InputObject('Amount (USD)', 'number')
result_display = Text('Converted Amount: N/A')

async def convert_currency(ctx: ButtonCallbackContext):
    amount = float(await amount_input.get_value())
    async with aiohttp.ClientSession() as session:
        result_display.label = f'Converted Amount: Loading... (please wait, API is slow)'
        result_display.update()
        async with session.get('https://api.exchangerate-api.com/v4/latest/USD') as response:
            data = await response.json()
            conversion_rate = data['rates']['EUR']
            result_display.label = f'Converted Amount: {amount * conversion_rate:.2f} EUR'
            result_display.update()

convert_button = Button('Convert to EUR', on_click=convert_currency)

page.add(
    amount_input, result_display, convert_button
)

if __name__ == '__main__':
    page.run_in_desktop('D:\\nwjs\\nw.exe', title='Currency Converter')
