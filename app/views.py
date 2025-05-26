from django.shortcuts import render
import requests

from app.models import CitySearch

headers = {'User-Agent': 'DjangoWeatherApp/1.0'}


def weather(request):
    if not request.session.session_key:
        request.session.save()

    city = request.GET.get('city')
    context = {}

    if city:
        try:
            request.session['last_city'] = city

            lan, lon = define_latitude_longitude(city)
            data = define_weather(lan, lon)
            if data:
                obj, created = CitySearch.objects.get_or_create(city=city)
                obj.count += 1
                obj.save()

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

    else:
        last_city = request.session.get('last_city')
        if last_city:
            context['info'] = f"Вы ранее искали: {last_city}"

    return render(request, 'weather.html', context)


def define_latitude_longitude(city):
    req = requests.get(f'https://nominatim.openstreetmap.org/search?city={city}&format=json', headers=headers)
    if req.status_code != 200:
        raise Exception("Ошибка запроса к геокодеру")
    data = req.json()
    if not data:
        raise ValueError(f"Город '{city}' не найден")
    defined = data[0]
    return defined['lat'], defined['lon']


def define_weather(lan, lon):
    req = requests.get(
        f'https://api.open-meteo.com/v1/forecast?latitude={lan}&longitude={lon}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m')
    return req.json()


def HistoryView(request):
    data = CitySearch.objects.all().order_by('-count')
    return render(request, template_name='history.html', context={'data': data})
