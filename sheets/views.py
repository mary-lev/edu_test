from django.shortcuts import render

#from .utils import df, students
from .lesson_1 import values, students
from .parse_sheets import result

def index(request):
	return render(request, 'sheets/index.html', {'values': values, 'students': students})

def parse_json(request):
	return render(request, 'sheets/lesson.html', {'result': result})
