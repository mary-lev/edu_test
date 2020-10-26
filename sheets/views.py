import json
from django.shortcuts import render

#from .utils import df, students
#from .lesson_1 import values, students
#from .parse_sheets import result
from .feedback import first_lesson
#from .pyggy import sh

def index(request):
	return render(request, 'sheets/index.html', {
		#'values': values,
		'students': first_lesson,
		})

def get_feedbacks(request):
	filenames = ['mio4_lesson1.json', 'mio4_lesson2.json', 'mio4_lesson3.json',
			'mio4_lesson4.json', 'mio4_lesson5.json', 'mio4_lesson6.json',
			'mio4_lesson7.json'
			]
	feedbacks = list()
	for filename in filenames:
		with open(filename, 'r') as f:
			text = json.load(f)
			feedbacks += text
	return render(request, 'sheets/feedbacks.html', {'feedbacks': feedbacks})

def parse_json(request):
	return render(request, 'sheets/lesson.html', {'result': result})
