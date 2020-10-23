from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms
from django.forms import ModelChoiceField
from django.forms import modelformset_factory

from .models import Task, Solution, Variant, Question


def create_solution_formset(task):
	formset = []

	return formset



def make_question_formset(question, extra=0):
	class _VariantForm(forms.ModelForm):
		variants = ModelChoiceField(
			queryset=Variant.objects.filter(question=question).values_list('text', flat=True).distinct(),
			widget=forms.RadioSelect(),
			empty_label=None,
			label=question.question_text
			)
		
		class Meta:
			model = Question
			fields = ['variants']

	return _VariantForm

class VariantSomeForm(forms.ModelForm):
	class Meta:
		model = Variant
		fields = "__all__"
		widgets = {
		'text': forms.RadioSelect(attrs={'class': 'mb-0'})
		}


class QuestionForm(forms.ModelForm):
	variants = forms.ModelChoiceField(
		queryset=Variant.objects.values_list('text', flat=True).distinct(),
		widget=forms.RadioSelect)
	class Meta:
		model = Question
		fields = ['variants']


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['variants'].label_class='mb-0'

		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.add_input(Submit('submit',
			'Готово',
			css_class='btn btn-info mt-4 mb-2'))

		self.helper.form_class = 'card mt-4 mb-3'
		self.helper.label_class = 'display-4'



