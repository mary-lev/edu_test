import json
import string
import pandas as pd
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django import forms
from django.db.models import Count
  
from django.contrib import messages
from django.forms import modelformset_factory
import csv

from .visual import date_div, dn
from .models import Student, Lesson, Module, Stream, Task, Feedback, Solution, Question, Variant

from .feedback import create_graph
from .tone import create_new_graph
from .forms import QuestionForm, make_question_formset, create_solution_formset


def index(request):
	streams = Stream.objects.all()
	return render(request, 'index.html', {'streams': streams})

def tone(request):
	div = create_new_graph()
	return render(request, 'tone.html', {'div': div})


def get_solution(request, task_id):
	task = Task.objects.get(id=task_id)
	form = create_solution_formset(task)

	return render(request, 'solution2.html', {'form': form, 'task': task})


def new_solution(request, task_id):
	task = Task.objects.get(id=task_id)
	questions = Question.objects.filter(task=task)
	formsets = []
	for question in questions:
		#if all.question_type=='Radiobutton':
		VariantFormSet = make_question_formset(question)
		if request.method == 'POST':
			myformset = VariantFormSet(request.POST,
				prefix=question.id)
			if myformset.is_valid():
				myformset.save()
		else:
			myformset = VariantFormSet(
				prefix=question.id)
		formsets.append(myformset)
	return render(request,
		'solution1.html',
		{'formset': formsets, 'questions': questions, 'task': task})



class StudentView(DetailView):
	model = Student


class TaskView(DetailView):
	model = Task
	template_name = 'task.html'


class TaskSolution(FormMixin, DetailView):
	model = Task
	form_class = QuestionForm
	template_name = 'solution.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'].fields['variants'].queryset = Variant.objects.filter(
			question=self.object.questions.all()[0].id).values_list('text', flat=True)
		context['form'].fields['variants'].label = self.object.questions.all()[0].question_text
		context['form'].fields['variants'].label_class = 'mb-0'
		return context


class LessonView(DetailView):
	model = Lesson


class ModuleView(DetailView):
	model = Module

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['div'] = create_graph(self.object)
		return context


class StreamView(DetailView):
	model = Stream

TOLSTOY = 461688
def count_words(request):
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
		tolstoy = round((student_words*100)/TOLSTOY, 2)
		students_texts.append([student, student_text, student_words, tolstoy])
	all_tolstoy = round((all_tolstoy*100)/TOLSTOY, 1)
	students_texts = sorted(students_texts, key=lambda x: x[3], reverse=True)
	return render(request, 'count_words.html', {'data': students_texts, 'tolstoy': all_tolstoy})


class SolutionAll(ListView):
	#tasks =[2, 6, 8, 10, 12, 16, 21, 24, 25, 29, 30, 31, 32, 33, 36, 37, 38, 46, 48, 50, 52, 56, 
	#		57, 60, 62, 63, 64, 66, 67, 68, 69, 70, 71, 73, 75, 76, 79, 80, 86, 88, 89, 90, 92,
	#		94, 95, 97, 98, 99, 104, 105, 106, 107, 108, 109, 110, 111, 114, 115, 117, 120, 123, 125,
	#		126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 
	#		145, 146, 147, 148, 149, 150, 151, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165]
	#10 - cit/links
	#24 - adress
	#48 - dictionaries
	#50 - orfo rules
	#117 - link
	#138 - link
	#141 - maybe link
	#142 - time
	#144 - vacancy/edit
	#148 - link
	#151 - speed typing
	#153 - link


	model = Solution

	def get_queryset(self):
		return Task.objects.filter(lesson__module__name='Тексты').annotate(num_task=Count('solutions'))


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
    percents_columns = [0, 4,17,39,61,83,102,126,147,170,201]
    percents = df.iloc[:, percents_columns]
    dn = df.iloc[:, columns]
    return render(request, 'index.html', {
    	'messages': dn.to_html(),
    	'df': df.itertuples(),
    	'percents': percents.to_html()})


def parse(request):
	with open('sce_solutions2.json', 'r') as f:
		solutions = json.load(f)
	for solution in solutions:
		task = Task.objects.get(number=int(solution['task']), lesson__module__name='Сценарии')
		student, create = Student.objects.get_or_create(
			first_name=solution['name'],
			last_name=solution['family'],
			email=solution['email'])
		new_solution = Solution.objects.create(task=task, student=student, text=solution['text'])
	return render(request, 'parse.html', {'data': solutions})

def parse3(request):
	with open('scen_task.json', 'r') as f:
		tasks = json.load(f)
	for all in tasks:
		text_tasks = Task.objects.filter(lesson__module__name='Сценарии')
		task = text_tasks.get(number=int(all['number']))
		task.name = all['title']
		task.text = all['text']
		task.save()
	return render(request, 'parse.html', {'data': tasks})

def parse2(request):
	with open('texts1.json', 'r') as f:
		users = json.load(f)
	tasks = list()
	for all in users:
		module, create = Module.objects.get_or_create(name='Тексты')
		stream, create = Stream.objects.get_or_create(
			name='Июнь', module=module)
		lesson, create = Lesson.objects.get_or_create(module=module, number=int(all['lesson']))
		student, create = Student.objects.get_or_create(
			email=all['email'],
			first_name=all['name'],
			last_name=all['family']
			)
		student.stream.add(stream)
		task, create = Task.objects.get_or_create(
			number='task'+all['number'], lesson=lesson)
		if all['solution']:
			solution, create = Solution.objects.get_or_create(
				task=task,
				student=student,
				text=all['solution']
				)
		if all['text']:
			feedback, create = Feedback.objects.get_or_create(
				student=student,
				task=task,
				text=all['text'])
		tasks.append(task)
	return render(request, 'parse.html', {'data': tasks})


def parse1(request):
	df = pd.read_json('scenario1.json')
	users = list()
	for index, row in df.iterrows():
		module, create = Module.objects.get_or_create(
			name='Сценарии', slug='scenario')
		stream, create = Stream.objects.get_or_create(
			name='Апрель', module=module)
		student, create = Student.objects.get_or_create(
			email=row['email'],
			first_name=row['name'],
			last_name=row['last_name'])
		for x in range(1, 156):
			if x == 131:
				one = 'task' + str(x)
				task, create = Task.objects.get_or_create(
					number=one,
					)
				if row[one]:
					feedback, create = Feedback.objects.get_or_create(
						student=student,
						task=task,
						text=row[one])

		users.append(row['email'])

	return render(request, 'parse.html', {'data': users})
	

class DateGraph(TemplateView):
    template_name = 'telegram.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_div'] = date_div
        context['dn'] = dn
        return context
