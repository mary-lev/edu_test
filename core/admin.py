from django.contrib import admin

from .models import Student, Stream, Module, Task, Lesson, Feedback, Solution


class StudentAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email')


class LessonAdmin(admin.ModelAdmin):
	list_display = ('number', 'module')


class StreamAdmin(admin.ModelAdmin):
	list_display = ('name', 'module')


class TaskAdmin(admin.ModelAdmin):
	list_display = ('number', 'name', 'lesson')
	list_filter = ('lesson',)


class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('task', 'student', 'text', 'get_lesson', 'get_module')
	list_filter = ('task__lesson',)

	def get_lesson(self, obj):
		return obj.task.lesson

	def get_module(self, obj):
		return obj.task.lesson.module


class SolutionAdmin(admin.ModelAdmin):
	list_display = ('task', 'student', 'text')



admin.site.register(Student, StudentAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(Module)
admin.site.register(Task, TaskAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Solution, SolutionAdmin)
