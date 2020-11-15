from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from django.forms import modelformset_factory, formset_factory, BaseModelFormSet

from .models import Variant, Question, Feedback, Task


"""forms for task solutions"""
def choice_form(questions):
    if len(questions) != 1:
        VariantForm = create_formset2(questions)
        print("questions", questions)
    else:
        if questions[0].question_type == '2':
            VariantForm = make_checkbox_formset(questions[0])
        elif questions[0].question_type == '3':
            VariantForm = make_task_form(questions[0])
        else:
            VariantForm = make_question_formset(questions[0])
    return VariantForm


def create_formset(questions):
    class _NormalForm(forms.Form):
        question = forms.CharField()
        variants = forms.ChoiceField(widget=forms.RadioSelect(), choices=(1, 2, 3))

    initial = list()
    for question in questions:
        point = dict()
        point['question'] = question.question_text
        point['label'] = question.question_text
        point['variants'] = {}
        point['variants']['choices'] = [(var.id, var.text) for var in (Variant.objects.filter(question=question))]
        initial.append(point)
    print(initial)

    QuestionFormSet = formset_factory(_NormalForm, extra=0)
    formset = QuestionFormSet(initial=initial)
    return formset

def create_formset2(questions, extra=0):
    class _VariantForm(CrispyModelForm):
        variants = VariantModelChoiceField(
            queryset=Variant.objects.filter(question=questions[0]),
            to_field_name='text',
            widget=forms.RadioSelect(),
            empty_label=None,
            #label=question.question_text
        )

        class Meta:
            model = Question
            fields = ['variants']
    
    class _BaseQuestionFormSet(BaseModelFormSet):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.queryset = Variant.objects.filter(question=self.obj)

    QuestionFormSet = modelformset_factory(Question, _VariantForm, extra=0)
    formset = QuestionFormSet(queryset=questions)
    return formset

"""create crispy design for all modelforms"""
class CrispyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit',
            'Готово',
            css_class='btn btn-info mt-4 mb-2'))
        self.helper.form_class = 'card mt-4 mb-3'
        self.helper.label_class = 'display-4'

"""form for radiobuttons"""
class VariantModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.text


def make_question_formset(question, extra=0):
    class _VariantForm(CrispyModelForm):
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

    return _VariantForm

"""form for checkbox multiple select"""
class VariantModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.text


def make_checkbox_formset(question, extra=0):
    class _VariantForm(CrispyModelForm):
        variants = VariantModelMultipleChoiceField(
            queryset=Variant.objects.filter(question=question).distinct(),
            to_field_name='text',
            widget=forms.CheckboxSelectMultiple,
            #empty_label=None,
            label=question.question_text
        )

        class Meta:
            model = Question
            fields = ['variants']

    return _VariantForm

"""form for textarea"""
def make_task_form(question, extra=0):
    class _QuestionForm(CrispyModelForm):
        answer = forms.CharField(
            widget=forms.Textarea(attrs={"rows":5, "cols":40, 'class': 'mb-0'}),
            label=question.question_text
            )
        class Meta:
            model = Question
            fields = ('answer',)

    return _QuestionForm


"""other forms"""
class TaskFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label_class = 'mb-0'
        self.fields['text'].label = "Комментарий к задаче (пишите всё, что хотите):"
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit',
            'Готово',
            css_class='btn btn-info mt-4 mb-2'))
        self.helper.form_class = 'card mt-4 mb-3'


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
