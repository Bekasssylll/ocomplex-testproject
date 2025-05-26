from django.contrib import admin
from django.urls import path, include
from app.views import weather, HistoryView
urlpatterns = [
    path("", weather,name='weather'),
    path('history/',HistoryView,name='history')
]
