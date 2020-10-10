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
	lesson = models.ForeignKey(Lesson)
	text = models.TextField()
	mark_max = models.IntegerField()


class Task(models.Model):
	task_group = models.ForeignKey(TaskGroup)
	text = models.TextField()
	question = models.TextField()
	picture = models.ImageField()
	solution = models.TextField()


class Solution(models.Model):
	task = models.ForeignKey(Task)
	text = models.CharField()
	student = models.ForeignKey(Student)
	mark = models.IntegerField()


class Feedback(models.Model):
	student = models.ForeignKey(Student)
	task_group = models.ForeignKey(TaskGroup)
