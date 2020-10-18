import json
import pandas as pd
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView

from .visual import date_div, dn
from .models import Student, Lesson, Module, Stream, Task, Feedback, Solution

from .feedback import create_graph


def index(request):
	all_tasks = Task.objects.all()
	module = Module.objects.all().first()
	return render(request, 'index.html', {'tasks': all_tasks, 'div': create_graph(module)})

class StudentView(DetailView):
	model = Student


class TaskView(DetailView):
	model = Task


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
