from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Naran Primeiru',
            'last_name': 'Naran Ikus',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            'email',
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="{% url \'user-profile\' %}" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class ProfilePasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password Atuál',
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label='Password Foun',
        min_length=8,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label='Konfirma Password Foun',
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'old_password',
            Row(
                Column('new_password1', css_class='col-md-6'),
                Column('new_password2', css_class='col-md-6'),
            ),
            Submit('submit', 'Muda Password', css_class='btn btn-primary'),
            HTML('<a href="{% url \'user-profile\' %}" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Password atuál la loos.')
        return old_password

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password1')
        p2 = cleaned.get('new_password2')
        if p1 and p2 and p1 != p2:
            self.add_error('new_password2', 'Password foun la hanesan.')
        return cleaned
