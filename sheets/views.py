from django.shortcuts import render

from .utils import values, df

def index(request):
	return render(request, 'sheets/index.html', {'values': df})
