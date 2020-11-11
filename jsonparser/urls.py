from django.contrib import admin
from django.urls import path, include

from . import views

app_name ='jsonparser'
urlpatterns = [
	path('', views.index, name='index'),
	]