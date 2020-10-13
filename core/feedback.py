import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as opy

from django.db.models import Count

from .models import Feedback, Task

feedbacks = Task.objects.annotate(num_feedback=Count('feedbacks'))
tasks = [all.number for all in feedbacks]
feed = [all.num_feedback for all in feedbacks]



fig = px.line(feedbacks, x=tasks, y=feed, title='Число фидбэков по задачам')


div = opy.plot(fig, auto_open=False, output_type='div')