from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from django.forms import modelformset_factory, inlineformset_factory

from .models import Variant, Question, Feedback, Task, Solution


"""form for radiobuttons"""
class VariantModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.text


class VariantForm(forms.ModelForm):
	variants = VariantModelChoiceField(
		queryset=Variant.objects.none(),
		to_field_name='text',
		widget=forms.CheckboxSelectMultiple(),
		#empty_label=None,
		#label=form.instance.question_text
		)

	class Meta:
		model = Question
		fields = ['variants']
	
VariantFormSet = inlineformset_factory(
		Task,
		Question,
		form=VariantForm,
		fields = ('question_text', 'variants',),
		#formset=BaseModelFormSet,
		extra=0,
		)

SolutionFormSet = inlineformset_factory(
	Task,
	Solution,
	fields = ('task', 'variant',),
	form=VariantForm,
	extra=0
	)

def create_new_form(task):
	class NewForm(forms.ModelForm):
		class Meta:
			model = Solution
			questions = Question.objects.filter(task=task)
			fields = []
			for n, question in enumerate(questions):
				field = forms.MultipleChoiceField(
					choices=[(variant.id, variant.text) for variant in question.variants.all()])
				fields.append(field)

	#NewForm = type('NewForm', (forms.BaseForm,), {'base_fields': base_fields})
	print(NewForm)
	return NewForm
			

