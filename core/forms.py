from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelChoiceField
from django.forms import modelformset_factory

from .models import Variant, Question, Feedback, Task


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('task', 'lesson', 'text', 'student',)


FeedbackFormSet = modelformset_factory(
    Feedback,
    form=FeedbackForm,
    can_delete=True,
    widgets={'DELETE': forms.CheckboxInput()}
)


class VariantModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.text

class QuestionModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.question_text

def make_task_formset(task, extra=0):
    class _QuestionForm(forms.ModelForm):
        questions = QuestionModelChoiceField(
            queryset=Question.objects.filter(task=task).distinct(),
            to_field_name='question_text',
            widget=forms.RadioSelect(),
            )

        class Meta:
            model = Question
            fields = ('question_text',)
    return _QuestionForm


def make_question_formset(question, extra=0):
    class _VariantForm(forms.ModelForm):
        variants = VariantModelChoiceField(
            queryset=Variant.objects.filter(question=question).distinct(),
            to_field_name='text',
            widget=forms.RadioSelect(),
            empty_label=None,
            label=question.question_text
        )

        class Meta:
            model = Question
            fields = ['variants']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['variants'].label_class = 'mb-0'

            self.helper = FormHelper()
            self.helper.form_method = 'POST'
            self.helper.add_input(Submit('submit',
                                         'Готово',
                                         css_class='btn btn-info mt-4 mb-2'))

            self.helper.form_class = 'card mt-4 mb-3'
            self.helper.label_class = 'display-4'

    return _VariantForm


class QuestionForm(forms.ModelForm):
    answer = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))

    class Meta:
        model = Question
        fields = ('question_text', 'description',)
        widgets = {
            'answer': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['answer'].initial = ''
        self.fields['answer'].label = self.instance.question_text

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit',
                                     'Готово',
                                     css_class='btn btn-info mt-4 mb-2'))
        self.helper.form_class = 'card mt-4 mb-3'
        self.helper.label_class = 'display-4'
