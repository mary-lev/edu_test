from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms
from django.forms import ModelChoiceField

from .models import Task, Solution, Variant, Question


class VariantModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.id, obj.text


class QuestionForm(forms.ModelForm):
	#variants =VariantModelChoiceField(queryset=Variant.objects.all())
	class Meta:
		model = Question
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.add_input(Submit('submit',
			'Отправить отклик',
			css_class='btn btn-primary mt-4 mb-2'))

		self.helper.form_class = 'card mt-4 mb-3'
		self.helper.label_class = 'mb-1'



