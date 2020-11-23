import csv
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as opy

from django.db.models import Count

from .models import Feedback, Task, Stream


def create_new_graph():

	with open('data/my_train.csv', 'r', encoding='utf-8') as f:
		csvrows = csv.reader(f) 
		train = [all for all in csvrows]
	data = []
	fail = []
	for all in train:
		try:
			feed = Feedback.objects.get(text=all[0])
			one = [feed.task.number, all[0], all[1]]
			data.append(one)
		except:
			fail.append(all[0])

	data = sorted(data, key = lambda i: i[0])

	tasks = [all.number for all in Task.objects.filter(lesson__module__name='Тексты')]
	zeros = [0 for x in range(0, len(tasks))]

	positives = []
	negatives = []

	for task in tasks:
		positiv = 0
		negativ = 0
		for all in data:
			if all[0] == task and all[2] == 'positive':
				positiv += 1
			elif all[0] == task and all[2] == 'negative':
				negativ += 1
		positives.append(positiv)
		negatives.append(negativ)

	df = pd.DataFrame({'task': tasks, 'positive': positives, 'negative': negatives})
	df['text'] = df['task'].apply(lambda x: 'Задача {0}'.format(x))


	fig = go.Figure(go.Scatter(
	x=list(tasks),
	y=zeros,
	mode='markers',
	marker={"opacity": 0.1}))


	fig.add_trace(go.Scatter(x=df['task'], y=df['positive'], mode='lines', line_color='#237ce1', text=df['text'], name='спасибо'))
	fig.add_trace(go.Scatter(x=df['task'], y=df['negative'], mode='lines', line_color='#a4a5a5', text=df['text'], name='протест'))

	fig.update_layout(title='График фидбэка: модуль «Тексты»')

	div = opy.plot(fig, auto_open=False, output_type='div')

	return div
