from django.contrib import admin

from .models import Student, Stream, Module, Task, Lesson, Feedback

admin.site.register(Student)
admin.site.register(Stream)
admin.site.register(Module)
admin.site.register(Task)
admin.site.register(Lesson)
admin.site.register(Feedback)
