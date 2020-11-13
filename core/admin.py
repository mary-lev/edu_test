from django import forms
from django.contrib import admin

from .models import Student, Stream, Module, Task, Lesson, Feedback, Solution, Question, Variant


class VariantInline(admin.TabularInline):
    model = Variant


class VariantAdmin(admin.ModelAdmin):
    model = Variant
    list_display = ('text', 'question', 'get_task', )
    list_filter = ('question__task',)

    def get_task(self, obj):
        return obj.question.task


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ('task', 'get_lesson', 'question_type', 'question_text', 'mark', 'answers',)
    list_filter = ('task',)
    inlines = (VariantInline,)

    def get_lesson(self, obj):
        return obj.task.lesson


class QuestionInline(admin.TabularInline):
    model = Question


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ('stream__name', 'stream__module__name',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('number', 'module')


class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'module')


class StreamInline(admin.TabularInline):
    model = Stream


class LessonInline(admin.TabularInline):
    model = Lesson


class ModuleAdmin(admin.ModelAdmin):
    model = Module
    inlines = (StreamInline, LessonInline,)


class TaskForm1(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Task
        widgets = {
            'question_type': forms.widgets.Select(
                choices=(
                    (0, 'A'),
                    (1, 'B'),
                )
            )
        }


class TaskForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Task
        widgets = {
            'question_type': forms.widgets.TextInput(),

        }


class TaskAdmin(admin.ModelAdmin):
    model = Task
    form = TaskForm
    list_display = ('number', 'name', 'lesson')
    list_filter = ('lesson',)
    inlines = (QuestionInline,)

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        if db_field.name == 'question_type':
            kwargs['widget'].choices = (('', '---------'), ('1', 'Choice1'), ('2', 'Choice2'))
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'text', 'get_lesson', 'get_module')
    list_filter = ('task__lesson', 'student',)

    def get_lesson(self, obj):
        return obj.task.lesson

    def get_module(self, obj):
        return obj.task.lesson.module


class SolutionVariantInline(admin.TabularInline):
    model = Solution.variant.through


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'text')
    list_filter = ('task__lesson', 'task')
    inlines = (SolutionVariantInline,)
    exclude = ('variant',)


admin.site.register(Student, StudentAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Variant, VariantAdmin)
