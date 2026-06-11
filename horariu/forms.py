from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import Horas, Horariu


class HorasForm(forms.ModelForm):
    class Meta:
        model = Horas
        fields = ['horas_hahu', 'horas_termina', 'obs']
        widgets = {
            'horas_hahu': forms.TimeInput(attrs={'type': 'time'}),
            'horas_termina': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'horas_hahu': 'Oras Hahu',
            'horas_termina': 'Oras Termina',
            'obs': 'Observasaun',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('horas_hahu', css_class='col-md-6'),
                Column('horas_termina', css_class='col-md-6'),
            ),
            'obs',
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class HorariuForm(forms.ModelForm):
    class Meta:
        model = Horariu
        fields = [
            'loron', 'horas', 'departamento', 'classe', 'turma',
            'professor_materia', 'ano_academico', 'is_active', 'obs',
        ]
        labels = {
            'loron': 'Loron',
            'horas': 'Oras',
            'departamento': 'Departamentu',
            'classe': 'Klase',
            'turma': 'Turma',
            'professor_materia': 'Professor / Materia',
            'ano_academico': 'Ano Akademiku',
            'is_active': 'Ativu',
            'obs': 'Observasaun',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('loron', css_class='col-md-6'),
                Column('horas', css_class='col-md-6'),
            ),
            Row(
                Column('departamento', css_class='col-md-4'),
                Column('classe', css_class='col-md-4'),
                Column('turma', css_class='col-md-4'),
            ),
            Row(
                Column('professor_materia', css_class='col-md-6'),
                Column('ano_academico', css_class='col-md-6'),
            ),
            'obs',
            Row(
                Column('is_active', css_class='col-md-3 pt-4'),
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )
