from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username=forms.EmailField(max_length=64)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'E-mail'

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit(
            'submit',
            'Войти',
            css_class='btn btn-primary btn-lg btn-block'))

        self.helper.form_class = 'form-signin pt-5'
        self.helper.label_class = 'text-muted'


class RegisterForm(UserCreationForm):
    username = forms.EmailField(max_length=64, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields.pop('username')

        for fieldname in ['username', 'password1', 'password2', ]:
            self.fields[fieldname].help_text = None

        #self.fields['username'].label = 'E-mail'

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit(
            'submit',
            'Зарегистрироваться',
            css_class="btn btn-primary btn-lg btn-block"))

        self.helper.form_class = 'form-signin pt-5'
        self.helper.label_class = 'text-muted'