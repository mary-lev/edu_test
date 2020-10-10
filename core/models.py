from django.db import models


class Student(models.Model):
	email = models.EmailField()
	first_name = models.CharField()
	last_name = models.CharField()


class Module(models.Model):
	name = models.CharField()
	slug = models.SlugField()


class Lesson(models.Model):
	module = models.ForeignKey(Module)
	number = models.IntegerField()


class TaskGroup(models.Model):
	lesson = models.ForeignKey(Lesson)


class Task(models.Model):
	task_group = models.ForeignKey(TaskGroup)
	text = models.TextArea()
	question = models.TextArea()
	picture = models.ImageField()


class Solution(models.Model):
	task = models.ForeignKey(Task)
	text = models.CharField()

	

