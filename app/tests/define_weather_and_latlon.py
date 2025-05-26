import sys
import os

import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()
from django.test import TestCase
from unittest.mock import patch
from app.views import define_latitude_longitude, define_weather


class ExternalAPITests(TestCase):

    @patch('app.views.requests.get')
    def test_define_latitude_longitude(self, mock_get):
        mock_get.return_value.json.return_value = [
            {'lat': '51.5074', 'lon': '-0.1278'}
        ]

        lat, lon = define_latitude_longitude('London')

        self.assertEqual(lat, '51.5074')
        self.assertEqual(lon, '-0.1278')

        # Проверяем, что requests.get вызвался с правильным URL
        mock_get.assert_called_once_with(
            'https://nominatim.openstreetmap.org/search?city=London&format=json',
            headers={'User-Agent': 'DjangoWeatherApp/1.0'}
        )

    @patch('app.views.requests.get')
    def test_define_weather(self, mock_get):
        mock_response = {
            'current': {'temperature_2m': 20, 'wind_speed_10m': 5},
            'current_units': {'temperature_2m': '°C', 'wind_speed_10m': 'km/h'},
            'hourly': {
                'time': ['2025-05-26T10:00', '2025-05-26T11:00'],
                'temperature_2m': [20, 21],
                'relative_humidity_2m': [50, 55],
                'wind_speed_10m': [5, 6]
            }
        }

        mock_get.return_value.json.return_value = mock_response

        result = define_weather('51.5074', '-0.1278')

        self.assertEqual(result, mock_response)

        mock_get.assert_called_once_with(
            'https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'
        )
