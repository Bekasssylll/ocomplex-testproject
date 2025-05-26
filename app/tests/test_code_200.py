import sys
import os
from django.test import TestCase

import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()
from rest_framework.test import APITestCase
from django.urls import reverse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()


class HistoryAPITest(APITestCase):
    def test_history_view_returns_200(self):
        url = reverse('history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class WeatherViewTest(TestCase):
    def test_weather_view_returns_200(self):
        response = self.client.get(reverse('weather'))
        self.assertEqual(response.status_code, 200)
