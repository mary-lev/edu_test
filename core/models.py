import os
#import cv2
import numpy
from colorthief import ColorThief
from PIL import Image as img2
from django.db import models
from django.contrib.auth.models import User, Group
from tinymce.models import HTMLField
from edu_test.settings import BASE_DIR

class Company(models.Model):
	name = models.CharField(max_length=100)
	logo = models.ImageField()


class Module(models.Model):
	name = models.CharField(max_length=100, verbose_name='Название')
	slug = models.SlugField()
	author = models.ManyToManyField(User, related_name='modules')

	def __str__(self):
		return self.name


class Stream(models.Model):
	name = models.CharField(max_length=100, verbose_name='Название')
	module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='streams', verbose_name='Модуль')
	start = models.DateField(null=True)

	def __str__(self):
		return self.module.name + ' ' + self.name


class Student(models.Model):
	email = models.EmailField()
	phone = models.CharField(max_length=100, null=True, blank=True)
	first_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	company = models.ManyToManyField(Company, related_name="students", blank=True)
	stream = models.ManyToManyField(Stream, related_name='students')

	def __str__(self):
		return "{0} {1}".format(self.first_name, self.last_name)

	def get_image_index(self):
		images = Image.objects.filter(student=self.id).exclude(name='1').exclude(type='doc').exclude(
			type='application/x-zip-compressed')
		try:
			all_edges = round(sum([image.contours_edges() for image in images]) / len(images), 2)
		except ZeroDivisionError:
			all_edges = 0
		return all_edges, len(images)


class NewStudent(User):
	company = models.ManyToManyField(Company, related_name="newstudent", blank=True)
	stream = models.ManyToManyField(Stream, related_name="newstudents", blank=True)


class Lesson(models.Model):
	module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
	number = models.IntegerField()
	theory = HTMLField()

	def __str__(self):
		return "{0} {1}".format(self.module, self.number)

	def next_lesson(self):
		return Lesson.objects.get(number=self.number+1, module=self.module).id


class Task(models.Model):
	TASK_TYPES = (
		('1', 'Radiobutton'),
		('2', 'Checkbutton'),
		('3', 'TextArea'),
		('4', 'OneCheckbox'),
		)
	number = models.IntegerField()
	name = models.CharField(max_length=200, blank=True)
	#module = models.ForeignKey(Module, default=1, on_delete=models.CASCADE)
	lesson = models.ForeignKey(
							Lesson,
							on_delete=models.CASCADE,
							blank=True,
							related_name='tasks'
							) # связь с группой задач
	text = HTMLField() # формулировка задачи
	hint = models.CharField(blank=True, null=True, max_length=1000)
	task_type = models.CharField(choices = TASK_TYPES, blank=True, null=True, max_length=1) # тип задачи (сделать список: выбор, вписать ответ)
	options = models.TextField(blank=True) # поле для хранения опций, если вопрос - выбор
	picture = models.URLField(blank=True, null=True) # картинка из шаблона
	picture_title = models.CharField(blank=True, null=True, max_length=200)
	our_solution = models.TextField(blank=True) # образцовое решение
	mark = models.IntegerField(blank=True, null=True) # количество баллов за задачу (здесь или в Solution?)

	def __str__(self):
		return self.lesson.module.name + " " + str(self.number)

	def next_task(self):
		try:
			result = Task.objects.get(number=str(int(self.number) + 1), lesson__module=self.lesson.module).id
		except:
			result = Task.objects.get(
				number=str(int(self.number) + 1),
				lesson__number=self.lesson.number +1,
				lesson__module=self.lesson.module).id
		return result

	def show_picture(self):
		if 'open?id=' in self.picture:
			return self.picture.replace('open?id=', 'uc?id=').replace('/view', '').replace('?usp=sharing', '')
		else:
			return self.picture.replace('file/d/', 'uc?id=').replace('/view', '').replace('?usp=sharing', '')

	class Meta:
		ordering = ['number']


class Question(models.Model):
	task = models.ForeignKey(Task, related_name='questions', on_delete=models.CASCADE)
	QUESTION_TYPES = (
		('1', 'Radiobutton'),
		('2', 'Checkbutton'),
		('3', 'TextArea'),
		('4', 'OneCheckbox'),
		)
	question_type = models.CharField(max_length=1, choices = QUESTION_TYPES, verbose_name='Тип вопроса')
	question_text = models.CharField(max_length=1000)
	description = models.CharField(max_length=1000, null=True, blank=True)
	mark = models.IntegerField(default=0)

	def __str__(self):
		return self.question_text


class Variant(models.Model):
	question = models.ForeignKey(Question, related_name='variants', on_delete=models.CASCADE)
	is_right = models.BooleanField(verbose_name='Верный ответ?')
	text = models.CharField(max_length=300)
	mark = models.IntegerField(default=0)

	def __str__(self):
		return self.text


class Solution(models.Model): # решение конкретной задачи конкретным студентом
	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='solutions') # связь с задачей
	text = models.CharField(max_length=100, null=True, blank=True) # решение
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='solutions') # связь со студентом
	mark = models.IntegerField(default=0) # количество полученных баллов
	variant = models.ManyToManyField(Variant, related_name='solutions')


class Feedback(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
	task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, related_name='feedbacks')
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, related_name='feedbacks')
	text = models.TextField(null=True)
	seen = models.BooleanField(verbose_name="Просмотрено", default=False)
	#lesson_help = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, related_name='feedbacks')

	def __str__(self):
		return self.text


class Image(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images')
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='images')
	url = models.URLField()
	name = models.ImageField(upload_to='data')
	type = models.CharField(max_length=10)
	contours = models.IntegerField(default=0)
	edges = models.IntegerField(default=0)
	size = models.CharField(max_length=100)

	def __str__(self):
		return self.name.url

	def get_area(self):
		width, height, _ = self.size.replace('(', '').replace(')', '').split(', ')
		area = int(width) * int(height)
		return int(area / self.contours)

	def get_width(self):
		width, height, _ = self.size.replace('(', '').replace(')', '').split(', ')
		return int(width)

	def get_height(self):
		width, height, _ = self.size.replace('(', '').replace(')', '').split(', ')
		return int(height)

	def contours_edges(self):
		return round(self.contours / self.edges, 2)

	"""def get_contours(self):
		if self.name != '1' and self.type != 'doc' and self.type != 'application/x-zip-compressed':
			img = cv2.imdecode(numpy.fromstring(self.name.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
			self.size = img.shape
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			ret, thresh4 = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO)
			contours, hierarchy = cv2.findContours(thresh4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			edges = cv2.Canny(thresh4, 100, 120)
			cnts, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
			self.edges = len(edges)
			self.contours = len(contours)
			self.save()
			return (len(contours), len(edges))
		else:
			return '1'"""

