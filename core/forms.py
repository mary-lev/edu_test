from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms

from .models import Task, Solution


class SolutionForm(forms.ModelForm):
	class Meta:
		model = Solution
		fields = ['text']
		widgets = {
		'task': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
		'text': forms.Textarea(attrs={'class': 'form-control'}),
		}


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		#self.fields['task'].label = self.kwargs.task.name

		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.label_class = 'mb-2 text-dark'
		self.helper.field_class = 'form-control'
