import json
import pandas as pd
from django.shortcuts import render
from django.views.generic import TemplateView

from .visual import date_div, dn

def index(request):
    df = pd.read_json('core/messages.json')

    return render(request, 'index.html', {'messages': df})


class DateGraph(TemplateView):
    template_name = 'telegram.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_div'] = date_div
        context['dn'] = dn
        return context
