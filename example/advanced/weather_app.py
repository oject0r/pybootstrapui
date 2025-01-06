"""
A weather application using Open-Meteo API to fetch data without requiring an API key.
"""

from pybootstrapui import Page, ButtonCallbackContext
from pybootstrapui import templates
from pybootstrapui.components import *
import aiohttp

page = Page(templates.Default)

city_input = InputObject('Enter Latitude, Longitude', 'text')  # Expecting coordinates (latitude, longitude)
weather_display = Text('Weather: N/A')


async def fetch_weather(ctx: ButtonCallbackContext):
	coords = await city_input.get_value()
	ctx.show_spinner()
	try:
		latitude, longitude = map(float, coords.split(','))  # Parse latitude and longitude
		async with aiohttp.ClientSession() as session:
			async with session.get(
					f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true') as response:
				if response.status == 200:
					data = await response.json()
					weather_info = data['current_weather']['weathercode']
					temperature = data['current_weather']['temperature']
					windspeed = data['current_weather']['windspeed']
					weather_display.label = (
						f"Current Weather:\n"
						f"- Weather Code: {weather_info}\n"
						f"- Temperature: {temperature}°C\n"
						f"- Wind Speed: {windspeed} km/h"
					)
				else:
					weather_display.label = f"Error: Unable to fetch weather data (HTTP {response.status})"
	except Exception as e:
		weather_display.label = f"Error: {str(e)}"
	ctx.hide_spinner()
	weather_display.update()


get_weather_button = Button('Get Weather', on_click=fetch_weather)

page.add(
	city_input,
	weather_display,
	get_weather_button
)

if __name__ == '__main__':
	page.run_in_desktop('/path/to/nwjs', title='Weather App (Open-Meteo)')
