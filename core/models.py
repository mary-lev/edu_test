from django.db import models
from django.contrib.auth.models import User, Group
from tinymce.models import HTMLField


"""class MyUser(AbstractUser):
	email = models.EmailField(max_length=64)
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	password = models.CharField(max_length=64)"""


class Company(models.Model):
	name = models.CharField(max_length=100)
	logo = models.ImageField()


class Module(models.Model):
	name = models.CharField(max_length=100, verbose_name='Название')
	slug = models.SlugField()

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
	text = models.TextField(blank=True) # формулировка задачи
	hint = models.CharField(blank=True, null=True, max_length=500)
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
		)
	question_type = models.CharField(max_length=1, choices = QUESTION_TYPES, verbose_name='Тип вопроса')
	question_text = models.CharField(max_length=1000)
	description = models.CharField(max_length=1000, null=True, blank=True)
	mark = models.IntegerField(default=0)
	answers = models.CharField(max_length=200)
	slug = models.SlugField()

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
	#lesson_help = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, related_name='feedbacks')

	def __str__(self):
		return self.text
