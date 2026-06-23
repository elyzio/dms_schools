from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import Ano, Departamento, Classe, Turma, Periodo, Materia


class AnoForm(forms.ModelForm):
    class Meta:
        model = Ano
        fields = ['ano', 'is_active']
        labels = {
            'ano': 'Ano',
            'is_active': 'Ativu',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('ano', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6 pt-4'),
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['departamento', 'sigla']
        labels = {
            'departamento': 'Departamentu',
            'sigla': 'Sigla',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('departamento', css_class='col-md-8'),
                Column('sigla', css_class='col-md-4'),
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['classe']
        labels = {
            'classe': 'Klase',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'classe',
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['turma']
        labels = {
            'turma': 'Turma',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'turma',
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['periodo', 'is_active']
        labels = {
            'periodo': 'Periodo',
            'is_active': 'Ativu',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('periodo', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6 pt-4'),
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['codigo', 'materia', 'departamentu', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'codigo': 'Codigo',
            'materia': 'Materia',
            'departamentu': 'Departamentu',
            'descricao': 'Deskrisaun',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='col-md-4'),
                Column('materia', css_class='col-md-8'),
            ),
            'departamentu',
            'descricao',
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )
