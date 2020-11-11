import plotly.graph_objs as go
import plotly.offline as opy
from django.db.models import Count

from .models import Task, Stream


def create_graph(module):
    all_tasks = Task.objects.filter(lesson__module=module).order_by('number').annotate(num_feedback=Count('feedbacks'))
    all_tasks_number = [all.number for all in all_tasks]
    all_feedacks = [0 for all in all_tasks_number]

    fig = go.Figure(go.Scatter(
        x=all_tasks_number,
        y=all_feedacks,
        mode='markers',
        marker={"opacity": 0.1},
        name=module.name))

    streams = Stream.objects.filter(module=module)

    for stream in streams:
        feedbacks_april = Task.objects.filter(
            feedbacks__student__stream=stream).order_by('number').annotate(num_feedback=Count('feedbacks'))
        tasks_april = [all.number for all in feedbacks_april]
        feed_april = [all.num_feedback for all in feedbacks_april]

        fig.add_trace(go.Scatter(x=tasks_april, y=feed_april, mode='lines', name=stream.name))

    fig.update_layout(title='Число фидбэков по задачам')

    div = opy.plot(fig, auto_open=False, output_type='div')

    return div
