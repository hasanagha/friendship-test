"""app URL Configuration"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('ftest.urls'), name='ftest'),
    path('admin/', admin.site.urls),
]
