from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'djangopotodds'

urlpatterns = [
    path('calculation/', calculate_view, name='calculation'),
    path('quiz/', quiz_view, name='quiz')
]