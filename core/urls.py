from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('parse/', views.parse, name='parse'),
    path('telegram/', views.DateGraph.as_view(), name='telegram'),
    ]