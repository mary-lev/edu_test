from django.db import models


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
		return self.name


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

	def __str__(self):
		return "{0} {1}".format(self.module, self.number)

	def next_lesson(self):
		return Lesson.objects.get(number=self.number+1, module=self.module)


class Task(models.Model):
	number = models.CharField(max_length=10)
	name = models.CharField(max_length=200, blank=True)
	#module = models.ForeignKey(Module, default=1, on_delete=models.CASCADE)
	lesson = models.ForeignKey(
							Lesson,
							on_delete=models.CASCADE,
							blank=True,
							related_name='tasks'
							) # связь с группой задач
	text = models.TextField(blank=True) # формулировка задачи
	question_type = models.TextField(blank=True) # тип задачи (сделать список: выбор, вписать ответ)
	options = models.TextField(blank=True) # поле для хранения опций, если вопрос - выбор
	picture = models.ImageField(blank=True) # картинка из шаблона
	our_solution = models.TextField(blank=True) # образцовое решение
	mark = models.IntegerField(blank=True, null=True) # количество баллов за задачу (здесь или в Solution?)

	def __str__(self):
		return self.number

	def next_task(self):
		return Task.objects.get(number='task' + str(int(self.number[4:]) + 1), lesson=self.lesson).id


	#class Meta:
		#ordering = ['number']


class Solution(models.Model): # решение конкретной задачи конкретным студентом
	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='solutions') # связь с задачей
	text = models.CharField(max_length=100) # решение
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='solutions') # связь со студентом
	mark = models.IntegerField(default=0) # количество полученных баллов


class Feedback(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
	task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, related_name='feedbacks')
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, related_name='feedbacks')
	text = models.TextField(null=True)
	#lesson_help = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, related_name='feedbacks')

	def __str__(self):
		return self.text
