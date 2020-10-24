from django.shortcuts import render

from .utils import values, df, students

def index(request):
	return render(request, 'sheets/index.html', {'values': df, 'students': students})
