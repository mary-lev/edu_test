import json
import pandas as pd
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from .visual import date_div, dn
from .models import Student, Lesson, Module, Stream, Task, Feedback

from .feedback import div


def index(request):
	all_tasks = Task.objects.all()
	return render(request, 'index.html', {'tasks': all_tasks, 'div': div})

class StudentView(DetailView):
	model = Student

class TaskView(DetailView):
	model = Task

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
	with open('scenario3.json', 'r') as f:
		users = json.load(f)
	tasks = list()
	for all in users:
		module = Module.objects.get(name='Сценарии')
		stream, create = Stream.objects.get_or_create(
			name='Июнь', module=module)
		student, create = Student.objects.get_or_create(
			email=all['email'],
			first_name=all['name'],
			last_name=all['family']
			)
		task, create = Task.objects.get_or_create(
			number='task'+all['number'])
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
