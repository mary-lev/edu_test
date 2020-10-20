import csv
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as opy

from django.db.models import Count

from .models import Feedback, Task, Stream


def create_graph():

	with open('my_train.csv', 'r', encoding='utf-8') as f:
		csvrows = csv.reader(f) 
		train = [all for all in csvrows]
	data = list()
	fail = list()
	for all in train[1:]:
		try:
			feed = Feedback.objects.get(text=all[0])
			one = {'task': feed.task.number, 'text': all[0], 'tone': all[1]}
			data.append(one)
		except:
			fail.append(all[0])
	data = sorted(data, key = lambda i: i['task'])

	positive = [all for all in data if all['tone']=='positive']
	negative = [all for all in data if all['tone']=='negative']
	tasks = [all['task'] for all in data]


	fig = go.Figure(go.Scatter(
	x=tasks,
	y=positive,
	mode='markers',
	marker={"opacity": 0.1},
	name='positive'))


	#fig.add_trace(go.Scatter(x=tasks_april, y=feed_april, mode='lines', name=stream.name))

	fig.update_layout(title='Позитив и негатив')

	div = opy.plot(fig, auto_open=False, output_type='div')

	return div
