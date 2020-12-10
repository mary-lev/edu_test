import json
import string
import csv
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.urls import reverse_lazy
from django import forms
from django.db.models import Count, Case, When, IntegerField
from django.forms import modelformset_factory

from rest_framework import viewsets

from .serializers import (StudentSerializer,
                          StreamSerializer,
                          ModuleSerializer,
                          LessonSerializer,
                          TaskSerializer,
                          FeedbackSerializer,
                          )
from .visual import date_div, dn
from .models import Student, Lesson, Module, Stream, Task, Feedback, Solution, Question, Variant

from .feedback import create_graph
from .tone import create_new_graph
from .forms import (
    choice_form,
    FeedbackForm,
    TaskFeedbackForm,
    QuestionFormSet,

)
from .user_forms import LoginForm, RegisterForm


# from .count_all import (is_link, compare_texts, get_address, count_words,
# analyze, analyze_one_student, count_tolstoy, compare_time, difficulty)


class MySignupView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('core:login')
    template_name = 'register.html'


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'


def index(request):
    streams = Stream.objects.all().order_by('module__name', 'name')
    return render(request, 'index.html', {'streams': streams})


def show_profile(request):
    feedbacks = Module.objects.filter(author=request.user).annotate(
        num_feedbacks=Count('lessons__tasks__feedbacks')).annotate(
        new=Count('lessons__tasks__feedbacks'))
    students = Module.objects.filter(author=request.user).annotate(num_students=Count('streams__students'))
    return render(request, 'profile.html', {'feedbacks': feedbacks, 'students': students})


def show_profile_module(request, module_id):
    module = Module.objects.get(id=module_id)
    feedbacks = Task.objects.filter(
        lesson__module__author=request.user,
        lesson__module=module).annotate(
        num_feedbacks=Count('feedbacks')).annotate(
        num_unseen=Count(
            Case(
                When(feedbacks__seen=False, then=1),
                output_field=IntegerField()
            )
        )
    )
    return render(request, 'profile_module.html', {'feedbacks': feedbacks, 'module': module})


class TaskFeedbackView(SingleObjectMixin, ListView):
    model = Feedback

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Task.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        return context

    def get_queryset(self):
        return self.object.feedbacks.all()


@login_required
@permission_required('core.add_solution')
def new_solution(request, task_id):
    """todo: Вынести валидацию в формы!"""
    task = Task.objects.get(id=task_id)
    formset = []
    if task.task_type == '1':
        template = 'solution2.html'
        formset = QuestionFormSet(instance=task)
    else:
        template = 'solution1.html'
        VariantForm = choice_form(task)
    questions = Question.objects.filter(task=task)
    student = Student.objects.get(id=128)
    solution, create = Solution.objects.get_or_create(student=student, task=task)
    if request.method == 'POST':
        solution.mark = 0
        solution.variant.clear()
        if task.task_type != '1':
            myformset = VariantForm(request.POST, prefix=questions[0].id)
            formset.append(myformset)
            if myformset.is_valid():
                if task.task_type == '3':
                    solution.text = myformset.cleaned_data['answer']
                    solution.mark = task.mark
                elif task.task_type == '2':
                    answers = myformset.cleaned_data['variants']
                    not_checked = task.questions.all()[0].variants.exclude(id__in=answers)
                    for answer in answers:
                        solution.variant.add(answer)
                        if answer.is_right:
                            solution.mark += answer.mark
                    for empty in not_checked:
                        if not empty.is_right:
                            solution.mark += empty.mark
                elif task.task_type == '4':
                    if myformset.cleaned_data['answer']:
                        solution.text = 'Done!'
                        solution.mark = task.mark
                solution.save()
                messages.add_message(
                    request,
                    messages.SUCCESS, "Ответ принят! Ваш балл {} из {}!".format(solution.mark, task.mark))
        else:
            try:
                formset = QuestionFormSet(request.POST, instance=task)
            except ValidationError:
                formset = None
            if formset and formset.is_valid():
                rooms = formset.save()
                solution = Solution.objects.get(task=task, student=student)
                messages.add_message(
                    request,
                    messages.SUCCESS, "Ответ принят! Ваш балл {} из {}!".format(solution.mark, task.mark)
                )
        return render(request, template, {
            'task': task,
            'formset': formset,
            'questions': questions
        })
    else:
        try:
            myformset = VariantForm(prefix=questions[0].id)
            formset.append(myformset)
        except:
            formset = QuestionFormSet(instance=task)
    return render(request,
                  template,
                  {'formset': formset, 'questions': questions, 'task': task})


mio_filenames = ['mio4_lesson_1.json', 'mio4_lesson_2.json', 'mio4_lesson_3.json',
                 'mio4_lesson_4.json', 'mio4_lesson_5.json', 'mio4_lesson_6.json',
                 'mio4_lesson_7.json'
                 ]


class Feedbackadding(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'add_feedbacks.html'
    success_url = '/add_feedbacks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_feedbacks = list()
        for filename in mio_filenames:
            with open(filename, 'r') as f:
                text = json.load(f)
                for feedback in text:
                    try:
                        feedback = Feedback.objects.get(text=feedback['feedback'])
                    except Feedback.DoesNotExist:
                        new_feedbacks.append(feedback)

        new = {}
        new['text'] = new_feedbacks[1]['feedback'][0]
        new['task'] = new_feedbacks[1]['task']
        new['lesson'] = new_feedbacks[1]['lesson']
        student, create = Student.objects.get_or_create(
            first_name=new_feedbacks[1]['student_name'],
            last_name=new_feedbacks[1]['student_family'],
            email=new_feedbacks[1]['student_email']
        )
        new['student'] = student.id
        form = FeedbackForm
        context['form'] = form(initial=new)
        # lesson = Lesson.objects.get(module__slug='mio', number=new['lesson'])
        # task = Task.objects.get(number=new, lesson=lesson)
        return context

        def post(self, request, *args, **kwargs):
            form = FeedbackForm(request.POST, initial=new)
            if form.is_valid():
                return self.form_valid(form)


class StudentView(DetailView):
    model = Student

    """def get_context_data(self, **kwargs):
                    context = super().get_context_data(**kwargs)
                    analytics = analyze_one_student(self.object.solutions.all())
                    grads = [all[1]['indexes']['grade_SMOG'] for all in analytics]
                    result = max(set(grads), key=grads.count)
                    tolstoy = count_tolstoy(self.object)
                    result = [analytics, result, tolstoy]
                    context['analytics'] = result
                    #context['grads'] = max(set(grads), key=grads.count)
                    return context"""


class TaskView(DetailView):
    model = Task
    template_name = 'task.html'


class FeedbackView(DetailView):
    model = Feedback


class LessonView(DetailView):
    model = Lesson


class ModuleView(DetailView):
    model = Module

    """def get_context_data(self, **kwargs):
                    context = super().get_context_data(**kwargs)
                    context['div'] = create_graph(self.object)
                    return context"""


class StreamView(DetailView):
    model = Stream


TOLSTOY = 461688


def tolstoy(request):
    stream = Stream.objects.filter(module__name='Тексты').values_list('students')
    students = Student.objects.filter(id__in=stream)
    solutions = Solution.objects.filter(task__lesson__module__name='Тексты')
    students_texts = []
    all_tolstoy = 0
    for student in students:
        student_text = solutions.filter(student=student).values_list('text', flat=True)
        student_words = 0
        for all in student_text:
            s = all.translate(str.maketrans('', '', string.punctuation))
            student_words += len(s.split(' '))
        all_tolstoy += student_words
        one_tolstoy = round((student_words * 100) / TOLSTOY, 2)
        students_texts.append([student, student_text, student_words, one_tolstoy])
    all_tolstoy = round((all_tolstoy * 100) / TOLSTOY, 1)
    students_texts = sorted(students_texts, key=lambda x: x[3], reverse=True)
    return render(request, 'count_words.html', {'data': students_texts, 'tolstoy': all_tolstoy})


"""show all solutions for one task"""


class SolutionTask(SingleObjectMixin, ListView):
    model = Solution

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Task.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        return context

    def get_queryset(self):
        return self.object.solutions.all()


"""show all solutions for module Texts"""


class SolutionAll(ListView):
    model = Solution

    def get_queryset(self):
        return Task.objects.filter(lesson__module__name='Тексты').annotate(num_task=Count('solutions'))


"""show all solutions if one student"""


class SolutionStudent(SingleObjectMixin, ListView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Student.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.object
        return context

    def get_queryset(self):
        return self.object.solutions.all()


class ModuleListView(ListView):
    model = Module


class StreamListView(ListView):
    model = Stream


class StudentListView(ListView):
    model = Student


def index1(request):
    df = pd.read_json('scenario1.json')
    columns = [all[0] for all in enumerate(df.columns.to_list())]
    exclude_columns = [3, 16, 36, 37, 38, 60, 82, 100, 101, 125, 145, 146, 169, 198, 199, 200]
    columns = [all for all in columns if all not in exclude_columns]
    percents_columns = [0, 4, 17, 39, 61, 83, 102, 126, 147, 170, 201]
    percents = df.iloc[:, percents_columns]
    dn = df.iloc[:, columns]
    return render(request, 'index.html', {
        'messages': dn.to_html(),
        'df': df.itertuples(),
        'percents': percents.to_html()})


"""рисуем граф телеграма"""


class DateGraph(TemplateView):
    template_name = 'telegram.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_div'] = date_div
        context['dn'] = dn
        return context


def tone(request):
    div = create_new_graph()
    return render(request, 'tone.html', {'div': div})


text_tasks = [2, 6, 8, 12, 16, 21, 24, 25, 29, 30, 31, 32, 33, 36, 37, 38, 46, 48, 50, 52, 56,
              57, 60, 62, 63, 64, 66, 67, 68, 69, 70, 71, 73, 75, 76, 79, 80, 86, 88, 89, 90, 92,
              94, 95, 97, 98, 99, 104, 105, 106, 107, 108, 109, 110, 111, 114, 115, 120, 123, 125,
              126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 139, 140, 142, 143, 144,
              145, 146, 147, 149, 150, 151, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165]
links = ['10', '117', '138', '141', '148', '153']


def analyze_task(request, task_id):
    task = Task.objects.get(id=task_id)
    solutions = Solution.objects.filter(task=task)
    answer = 'test'
    strange = ''
    # проверяем ссылку: 165
    if str(task.number) in ['10', '117', '138', '141', '148', '153']:
        answer = is_link(solutions)

    # сравниваем тексты: 283
    elif str(task.number) == '144':
        answer = compare_texts(solutions)

    # сравниваем время? 281
    elif str(task.number) == '142':
        answer = compare_time(solutions)

    # извлекаем адрес: 178
    elif str(task.number) == '24':
        answer = get_address(solutions)

    # считаем остальные тексты
    elif task.number in text_tasks:
        strange = count_words(solutions)
        answer = difficulty(solutions)
    else:
        answer = 'Здесь не нужно было ничего писать'

    return render(request, 'analyze_task.html', {'task': task, 'result': answer, 'strange': strange})


# API
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
