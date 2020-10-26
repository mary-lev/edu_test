import json
import pygsheets
import numpy as np

gc = pygsheets.authorize()

sh = gc.open('my new sheet')

with open('test_lesson_1.json', 'r') as f:
	result = json.load(f)

