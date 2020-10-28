from django.contrib import admin
from django.urls import path, include

from . import views

app_name ='core'
urlpatterns = [
	path('', views.index, name='index'),
	path('parse/', views.parse, name='parse'),
	path('tone/', views.tone, name='tone'),
	path('count_words/', views.tolstoy, name='count_words'),
	path('student/<pk>/', views.StudentView.as_view(), name='student'),
	path('students/', views.StudentListView.as_view(), name='students'),
	path('new_feedbacks/', views.get_new_feedbacks, name='new_feedbacks'),
	path('task/<pk>/', views.TaskView.as_view(), name='task'),
	path('task/<int:task_id>/analyze', views.analyze_task, name='analyze_task'),
	path('solutions/', views.SolutionAll.as_view(), name='solutions'),
	path('student/<pk>/solutions/', views.SolutionStudent.as_view(), name='student_solutions'),
	path('task/<pk>/solutions', views.SolutionTask.as_view(), name='task_solutions'),
	path('solution/<pk>/new/', views.TaskSolution.as_view(), name='solution'),
	path('solution1/<int:task_id>/new/', views.new_solution, name='solution1'),
	path('lesson/<pk>/', views.LessonView.as_view(), name='lesson'),
	path('module/<pk>/', views.ModuleView.as_view(), name='module'),
	path('modules/', views.ModuleListView.as_view(), name='modules'),
	path('stream/<pk>/', views.StreamView.as_view(), name='stream'),
	path('streams/', views.StreamListView.as_view(), name='streams'),
    path('telegram/', views.DateGraph.as_view(), name='telegram'),
    ]