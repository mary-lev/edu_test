from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms
from django.forms import ModelChoiceField

from .models import Task, Solution, Variant, Question


class VariantModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.id, obj.text
		

class QuestionForm(forms.ModelForm):
	variants =
	class Meta:
		model = Question
		fields = '__all__'
