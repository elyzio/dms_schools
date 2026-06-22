from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import Valor


class ValorForm(forms.ModelForm):
    class Meta:
        model = Valor
        fields = ['valor', 'obs']
        widgets = {
            'valor': forms.NumberInput(attrs={'step': '0.1', 'min': 0, 'max': 10}),
            'obs': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'valor': 'Valor (0 - 10)',
            'obs': 'Observasaun',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('valor', css_class='col-md-6'),
            ),
            'obs',
            Submit('submit', 'Grava', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )
