from django.contrib import admin
from django.urls import path, include

from . import views

app_name ='core'
urlpatterns = [
	path('', views.index, name='index'),
	path('parse/', views.parse, name='parse'),
	path('student/<pk>/', views.StudentView.as_view(), name='student'),
	path('task/<pk>/', views.TaskView.as_view(), name='task'),
    path('telegram/', views.DateGraph.as_view(), name='telegram'),
    ]