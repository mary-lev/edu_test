from django.db import models


class Company(models.Model):
	name = models.CharField()
	logo = models.ImageField()


class Student(models.Model):
	email = models.EmailField()
	phone = models.CharField()
	first_name = models.CharField()
	last_name = models.CharField()
	company = models.ManyToMany(Company, on_delete=models.CASCADE, related_name="students", null=True)
	stream = models.ManyToManyField(Stream) 


class Module(models.Model):
	name = models.CharField()
	slug = models.SlugField()


class Stream(models.Model):
	name = models.CharField()
	module = models.ForeignKey(Module)
	start = models.DateField()


class Lesson(models.Model):
	module = models.ForeignKey(Module)
	number = models.IntegerField()


class TaskGroup(models.Model):
	lesson = models.ForeignKey(Lesson) # связь с уроком
	text = models.TextField() # общий текст для группы задач
	#mark_max = models.IntegerField() # максимальное количество баллов за группу задач?


class Task(models.Model):
	task_group = models.ForeignKey(TaskGroup) # связь с группой задач
	text = models.TextField() # формулировка задачи
	question_type = models.TextField() # тип задачи (сделать список: выбор, вписать ответ)
	options = models.TextField() # поле для хранения опций, если вопрос - выбор
	picture = models.ImageField() # картинка из шаблона
	solution = models.TextField(null=True) # образцовое решение
	mark = models.IntegerField() # количество баллов за задачу (здесь или в Solution?)


class Solution(models.Model): # решение конкретной задачи конкретным студентом
	task = models.ForeignKey(Task) # связь с задачей
	text = models.CharField() # решение
	student = models.ForeignKey(Student) # связь со студентом
	mark = models.IntegerField(default=0) # количество полученных баллов


class Feedback(models.Model):
	student = models.ForeignKey(Student)
	task_group = models.ForeignKey(TaskGroup)
