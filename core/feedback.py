import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as opy

from django.db.models import Count

from .models import Feedback, Task, Stream

#feedbacks = Feedback.objects.filter(student__stream__name='Апрель').aggregate('task').count()
feedbacks = Task.objects.filter(feedbacks__student__stream__name='Апрель').annotate(num_feedback=Count('feedbacks'))
tasks = [all.number for all in feedbacks]
feed = [all.num_feedback for all in feedbacks]

stream = Task.objects.filter(feedbacks__student__stream__name='Июнь').annotate(num_feedback=Count('feedbacks'))
tasks1 = [all.number for all in feedbacks]
feed1 = [all.num_feedback for all in stream]


fig = px.line(feedbacks, x=tasks, y=feed, title='Число фидбэков по задачам')
fig.add_trace(go.Scatter(x=tasks, y=feed, mode='lines', name='Сценарии. Апрель'))
fig.add_trace(go.Scatter(x=tasks1, y=feed1, mode='lines', name='Сценарии. Июнь'))


div = opy.plot(fig, auto_open=False, output_type='div')