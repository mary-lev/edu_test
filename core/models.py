from django.db import models


class Company(models.Model):
	name = models.CharField(max_length=100)
	logo = models.ImageField()


class Module(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField()


class Stream(models.Model):
	name = models.CharField(max_length=100)
	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	start = models.DateField()


class Student(models.Model):
	email = models.EmailField()
	phone = models.CharField(max_length=100)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	company = models.ManyToManyField(Company, related_name="students")
	stream = models.ManyToManyField(Stream) 


class Lesson(models.Model):
	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	number = models.IntegerField()


class Task(models.Model):
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE) # связь с группой задач
	text = models.TextField() # формулировка задачи
	question_type = models.TextField() # тип задачи (сделать список: выбор, вписать ответ)
	options = models.TextField() # поле для хранения опций, если вопрос - выбор
	picture = models.ImageField() # картинка из шаблона
	our_solution = models.TextField(null=True) # образцовое решение
	mark = models.IntegerField() # количество баллов за задачу (здесь или в Solution?)


class Solution(models.Model): # решение конкретной задачи конкретным студентом
	task = models.ForeignKey(Task, on_delete=models.CASCADE) # связь с задачей
	text = models.CharField(max_length=100) # решение
	student = models.ForeignKey(Student, on_delete=models.CASCADE) # связь со студентом
	mark = models.IntegerField(default=0) # количество полученных баллов


class Feedback(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
