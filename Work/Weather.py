import sys
sys.path.append('../Work/api')

import requests
from api import my_api

api_key = my_api.api_open_weather_map
city = 'Yerevan'
lang = 'ru'
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang={lang}&units=metric'

response = requests.get(url)
data = response.json()

weather_description = data['weather'][0]['description']
temperature = data['main']['temp']
humidity = data['main']['humidity']

print(f'Today in {city}')
print(f'Descriptino: {weather_description.capitalize()}')
print(f'Temperature: {temperature}')
print(f'Humidity: {humidity}') 