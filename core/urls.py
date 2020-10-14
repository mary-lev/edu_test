from django.contrib import admin
from django.urls import path, include

from . import views

app_name ='core'
urlpatterns = [
	path('', views.index, name='index'),
	path('parse/', views.parse, name='parse'),
	path('student/<pk>/', views.StudentView.as_view(), name='student'),
	path('task/<pk>/', views.TaskView.as_view(), name='task'),
	path('lesson/<pk>/', views.LessonDetail.as_view(), name='lesson'),
	path('module/<pk>/', views.ModuleView.as_view(), name='module'),
	path('stream/<pk>/', views.StreamView.as_view(), name='stream'),
    path('telegram/', views.DateGraph.as_view(), name='telegram'),
    ]