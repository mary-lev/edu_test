from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib import messages
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from django.forms import (
    modelformset_factory,
    formset_factory,
    inlineformset_factory,
    BaseModelFormSet,
    BaseInlineFormSet
    )

from .models import Variant, Question, Feedback, Task, Solution


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
            queryset=Variant.objects.none(),
            to_field_name='text',
            widget=forms.RadioSelect(),
            empty_label=None,
            #label=question.question_text
        )

        class Meta:
            model = Question
            fields = ['variants']

    QuestionFormSet = modelformset_factory(
        Question,
        _VariantForm,
        extra=0
        )

    formset = QuestionFormSet(queryset=questions)
    for n, form in enumerate(formset.forms):
        form.fields['variants'].queryset = Variant.objects.filter(question=questions[n])
        form.fields['variants'].label = questions[n].question_text
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

class VariantForm(forms.ModelForm):
    variants = VariantModelChoiceField(
        queryset=Variant.objects.none(),
        to_field_name='text',
        widget=forms.RadioSelect,
        #empty_label=None,
        #label=question.question_text
        )
    class Meta:
        model = Question
        fields = ['variants']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['variants'].queryset = Variant.objects.filter(question=self.instance)


VariantFormSet = inlineformset_factory(
    Question,
    Variant,
    #formset=BaseVariantFormSet,
    fields=('text',),
    extra=0,
    can_delete=False,
    #widgets={'text': forms.RadioSelect},
    )

class BaseQuestionFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.nested = VariantForm(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            prefix='variant-%s' % (
                form.prefix,
                #VariantForm.get_default_prefix()
                ),
            )

    def is_valid(self):
        result = super().is_valid()
        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    print("Nested", form.nested)
                    result = result and form.nested.is_valid()
        return result

    def save(self, commit=True):
        result = super().save(commit=commit)
        solution, create = Solution.objects.get_or_create(student=128, task=self.instance)
        solution.variant.clear()
        mark = 0
        for form in self.forms:
            if hasattr(form, 'nested'):
                print('Question: ', form.cleaned_data['id'].id)
                print(form.nested)
                print(form.nested.cleaned_data['variants'])
                print(form.nested.cleaned_data['variants'].id)
                print(form.nested.cleaned_data['variants'].mark)
                solution.variant.add(form.nested.cleaned_data['variants'])
                mark += form.nested.cleaned_data['variants'].mark
                print(mark)
        solution.mark = mark        
        solution.save()
        return result

QuestionFormSet = inlineformset_factory(
    Task,
    Question,
    formset=BaseQuestionFormSet,
    fields=('question_text',),
    can_delete=False,
    extra=0)

"""['__class__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', 
'__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', 
'__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', 
'__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', 
'__subclasshook__', '__weakref__', '_get_choices', '_get_queryset', '_queryset', 
'_set_choices', '_set_queryset', 'bound_data', 'choices', 'clean', 'default_error_messages',
'default_validators', 'disabled', 'empty_label', 'empty_values', 'error_messages', 
'get_bound_field', 'get_limit_choices_to', 'has_changed', 'help_text', 'hidden_widget', 
'initial', 'iterator', 'label', 'label_from_instance', 'label_suffix', 'limit_choices_to', 
'localize', 'prepare_value', 'queryset', 'required', 'run_validators', 'show_hidden_initial',
 'to_field_name', 'to_python', 'valid_value', 'validate', 'validators', 'widget', 'widget_attrs']"""

"""['Meta', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__html__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_bound_fields_cache', '_clean_fields', '_clean_form', '_errors', '_get_validation_exclusions', '_html_output', '_meta', '_post_clean', '_save_m2m', '_update_errors', '_validate_unique', 'add_error', 'add_initial_prefix', 'add_prefix', 'as_p', 'as_table', 'as_ul', 'auto_id', 'base_fields', 'changed_data', 'clean', 'cleaned_data', 'data', 'declared_fields', 'default_renderer', 'empty_permitted', 'error_class', 'errors', 'field_order', 'fields', 'files', 'full_clean', 'get_initial_for_field', 'has_changed', 'has_error', 'hidden_fields', 'initial', 'instance', 'is_bound', 'is_multipart', 'is_valid', 'label_suffix', 'media', 'nested', 'non_field_errors', 'order_fields', 'prefix', 'renderer', 'save', 'use_required_attribute', 'validate_unique', 'visible_fields']"""


"""forms for task solutions"""
def choice_form(task):
    if task.task_type == 1:
        VariantForm = QuestionFormSet(instance=task)
        print(VariantForm)
    elif task.task_type == '2':
        print(task.questions.all())
        VariantForm = make_checkbox_formset(task.questions.all()[0])
    elif task.task_type == '3':
        VariantForm = make_task_form(task.questions.all()[0])
    else:
        VariantForm = make_question_formset(task.questions.all()[0])
    return VariantForm