from django.shortcuts import render
import requests

headers = {'User-Agent': 'DjangoWeatherApp/1.0'}


def test(request):
    city = request.GET.get('city')
    context = {}
    if city:
        try:
            lan, lon = define_latitude_longitude(city)
            data = define_weather(lan, lon)

            context = {
                'city': city,
                'current': data['current'],
                'temperature_unit': data['current_units']['temperature_2m'],
                'wind_unit': data['current_units']['wind_speed_10m'],
                'hourly': zip(
                    data['hourly']['time'][:24],
                    data['hourly']['temperature_2m'][:24],
                    data['hourly']['relative_humidity_2m'][:24],
                    data['hourly']['wind_speed_10m'][:24]
                )
            }
        except Exception as e:
            context['error'] = f"Ошибка при получении данных: {e}"

    return render(request, 'weather.html', context)


def define_latitude_longitude(city):
    req = requests.get(f'https://nominatim.openstreetmap.org/search?city={city}&format=json', headers=headers)
    data = req.json()
    defined = data[0]
    return defined['lat'], defined['lon']


def define_weather(lan, lon):
    req = requests.get(
        f'https://api.open-meteo.com/v1/forecast?latitude={lan}&longitude={lon}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m')
    return req.json()
