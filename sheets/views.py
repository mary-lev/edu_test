from django.shortcuts import render

from .utils import values

def index(request):
	return render(request, 'sheets/index.html', {'values': values})
