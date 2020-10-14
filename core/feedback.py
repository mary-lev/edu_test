import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as opy

from django.db.models import Count

from .models import Feedback, Task, Stream

all_tasks_number = [all.number for all in Task.objects.all()]
feedbacks = Task.objects.annotate(num_feedback=Count('feedbacks'))
all_feedacks = [all.num_feedback for all in feedbacks]

feedbacks_april = Task.objects.filter(
	feedbacks__student__stream__name='Апрель').annotate(num_feedback=Count('feedbacks'))
tasks_april = [all.number for all in feedbacks_april]
feed_april = [all.num_feedback for all in feedbacks_april]

feedbacks_june = Task.objects.filter(
	feedbacks__student__stream__name='Июнь').annotate(num_feedback=Count('feedbacks'))
tasks_june = [all.number for all in feedbacks_june]
feed_june = [all.num_feedback for all in feedbacks_june]

feedbacks_september = Task.objects.filter(
	feedbacks__student__stream__name='Сентябрь').annotate(num_feedback=Count('feedbacks'))
tasks_september = [all.number for all in feedbacks_september]
feed_september = [all.num_feedback for all in feedbacks_september]

test = [all for all in all_tasks_number if (all in tasks_april or all in tasks_june)]

fig = go.Figure(go.Scatter(
	x=all_tasks_number,
	y=all_feedacks,
	mode='markers',
	marker={"opacity": 0.1},
	name='Потоки'))
fig.add_trace(go.Scatter(x=tasks_april, y=feed_april, mode='lines', name='Сценарии. Апрель'))
fig.add_trace(go.Scatter(x=tasks_june, y=feed_june, mode='lines', name='Сценарии. Июнь'))
fig.add_trace(go.Scatter(x=tasks_september, y=feed_september, mode='lines', name='Сценарии. Сентябрь'))
fig.update_layout(title='Число фидбэков по задачам')

div = opy.plot(fig, auto_open=False, output_type='div')