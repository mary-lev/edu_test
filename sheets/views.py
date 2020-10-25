from django.shortcuts import render

#from .utils import df, students
from .lesson_1 import values, students

def index(request):
	return render(request, 'sheets/index.html', {'values': values, 'students': students})
