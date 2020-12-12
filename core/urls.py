from django.urls import path, include
from django.contrib.auth.views import LogoutView
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'modules', views.ModuleViewSet)
router.register(r'streams', views.StreamViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'feedbacks', views.FeedbackViewSet)

app_name = 'core'
urlpatterns = [
	path('', views.index, name='index'),
	path('register', views.MySignupView.as_view(), name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile/', views.show_profile, name='profile'),
	path('profile/detail/', views.ProfileDetailView.as_view(), name='profile_detail'),
	path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<int:module_id>/', views.show_profile_module, name='module_feedbacks'),
	path('tone/', views.tone, name='tone'),
	path('count_words/', views.tolstoy, name='count_words'),
	path('student/<pk>/', views.StudentView.as_view(), name='student'),
	path('students/', views.StudentListView.as_view(), name='students'),
    path('task/<pk>/solutions', views.SolutionTask.as_view(), name='task_solutions'),
	path('images/', views.ImageListView.as_view(), name='images'),
	path('students_images', views.StudentImageView.as_view(), name='students_with_images'),

	path('add_feedbacks/', views.Feedbackadding.as_view(), name='add_feedbacks'),
    path('task/<pk>/feedbacks', views.TaskFeedbackView.as_view(), name='task_feedbacks'),
	path('task/<pk>/', views.TaskView.as_view(), name='task'),
    path('feedback/<pk>/', views.FeedbackView.as_view(), name='feedback'),
	path('task/<int:task_id>/analyze', views.analyze_task, name='analyze_task'),
	path('solutions/', views.SolutionAll.as_view(), name='solutions'),
	path('student/<pk>/solutions/', views.SolutionStudent.as_view(), name='student_solutions'),
	path('solution1/<int:task_id>/new/', views.new_solution, name='solution1'),
	path('lesson/<pk>/', views.LessonView.as_view(), name='lesson'),
	path('module/<pk>/', views.ModuleView.as_view(), name='module'),
	path('modules/', views.ModuleListView.as_view(), name='modules'),
	path('stream/<pk>/', views.StreamView.as_view(), name='stream'),
	path('streams/', views.StreamListView.as_view(), name='streams'),
	path('telegram/', views.DateGraph.as_view(), name='telegram'),
	path('api/', include(router.urls)),
]
