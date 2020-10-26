from django.contrib import admin
from django.urls import path, include

from . import views

app_name ='sheets'
urlpatterns = [
	path('', views.index, name='index'),
	path('lesson', views.parse_json, name='lesson'),
	path('feedbacks', views.get_feedbacks, name='feedbacks'),
	]