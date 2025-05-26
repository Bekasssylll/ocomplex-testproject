from django.contrib import admin
from django.urls import path, include
from app.views import test

urlpatterns = [
    path("test/", test)
]
