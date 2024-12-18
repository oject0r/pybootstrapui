"""
A simple timer application to count down from a specified number of seconds.
"""

from pybootstrapui import Page, ButtonCallbackContext
from pybootstrapui import templates
from pybootstrapui.components import *
import asyncio

page = Page(templates.Default)

time_input = InputObject('Enter Time in Seconds', 'number')
timer_display = Text('Timer: 0')

async def start_timer(ctx: ButtonCallbackContext):
    time_remaining = int(await time_input.get_value())
    while time_remaining > 0:
        timer_display.label = f'Timer: {time_remaining}'
        timer_display.update()
        await asyncio.sleep(1)
        time_remaining -= 1
    timer_display.label = 'Time is up!'
    timer_display.update()

start_button = Button('Start Timer', callback=start_timer)

page.add(
    time_input, timer_display, start_button
)

if __name__ == '__main__':
    page.run_in_desktop('D:\\nwjs\\nw.exe', title='Simple Timer')
