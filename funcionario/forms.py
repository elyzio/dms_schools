from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, Submit, HTML
from .models import Professor, ProfessorUser, ProfessorClasse, ProfessorMateria


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = [
            'nome', 'sexu', 'data_moris', 'fatin_moris', 'nacionalidade',
            'eleitoral_prof', 'emis_prof',
            'distrito', 'subdistrito', 'suco', 'aldeia',
            'kontatu', 'hela_fatin', 'email',
            'estadu', 'posisaun_prof', 'nivel_akademiku', 'grau_akademiku',
            'numero_funcionario', 'data_contratacao', 'estadu_civil',
            'is_active', 'imagem',
        ]
        widgets = {
            'data_moris': forms.DateInput(attrs={'type': 'date'}),
            'data_contratacao': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'nome': 'Naran',
            'eleitoral_prof': 'No. Eleitoral',
            'emis_prof': 'No. EMIS',
            'estadu': 'Estatutu',
            'posisaun_prof': 'Pozisaun',
            'data_contratacao': 'Data Kontratu',
            'numero_funcionario': 'No. Funcionario',
            'nivel_akademiku': 'Nivel Akademiku',
            'grau_akademiku': 'Grau Akademiku'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informasaun Pessoal',
                Row(
                    Column('nome', css_class='col-md-6'),
                    Column('sexu', css_class='col-md-3'),
                    Column('estadu_civil', css_class='col-md-3'),
                ),
                Row(
                    Column('data_moris', css_class='col-md-4'),
                    Column('fatin_moris', css_class='col-md-4'),
                    Column('nacionalidade', css_class='col-md-4'),
                ),
                Row(
                    Column('eleitoral_prof', css_class='col-md-6'),
                    Column('emis_prof', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Enderesu & Kontatu',
                Row(
                    Column('distrito', css_class='col-md-6'),
                    Column('subdistrito', css_class='col-md-6'),
                ),
                Row(
                    Column('suco', css_class='col-md-6'),
                    Column('aldeia', css_class='col-md-6'),
                ),
                Row(
                    Column('kontatu', css_class='col-md-4'),
                    Column('email', css_class='col-md-4'),
                    Column('hela_fatin', css_class='col-md-4'),
                ),
            ),
            Fieldset(
                'Informasaun Profisionál',
                Row(
                    Column('estadu', css_class='col-md-4'),
                    Column('posisaun_prof', css_class='col-md-4'),
                    Column('numero_funcionario', css_class='col-md-4'),
                ),
                Row(
                    Column('nivel_akademiku', css_class='col-md-4'),
                    Column('grau_akademiku', css_class='col-md-4'),
                    Column('data_contratacao', css_class='col-md-4'),
                ),
                Row(
                    Column('is_active', css_class='col-md-3'),
                ),
            ),
            Fieldset(
                'Foto',
                'imagem',
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class ProfessorUserForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Konfirma Password')
    role = forms.ChoiceField(
        choices=[('admin', 'Admin'), ('professor', 'Professor'), ('diretor', 'Diretor')],
        label='Papel (Role)',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('role', css_class='col-md-6'),
            ),
            Row(
                Column('password1', css_class='col-md-6'),
                Column('password2', css_class='col-md-6'),
            ),
            Submit('submit', 'Kria Utilizador', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Password la hanesan.')
        username = cleaned.get('username')
        if username and User.objects.filter(username=username).exists():
            self.add_error('username', 'Username ne\'e uza tiha ona.')
        return cleaned


class ProfessorUserPasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password Foun')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Konfirma Password Foun')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('password1', css_class='col-md-6'),
                Column('password2', css_class='col-md-6'),
            ),
            Submit('submit', 'Troka Password', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Password la hanesan.')
        return cleaned


class ProfessorMateriaForm(forms.ModelForm):
    class Meta:
        model = ProfessorMateria
        fields = ['professor', 'materia', 'classe', 'is_active']
        labels = {
            'is_active': 'Ativu',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('professor', css_class='col-md-6'),
                Column('materia', css_class='col-md-6'),
            ),
            Row(
                Column('classe', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6 pt-4'),
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class ProfessorClasseForm(forms.ModelForm):
    class Meta:
        model = ProfessorClasse
        fields = ['professor', 'ano', 'departamento', 'classe', 'turma', 'is_class_teacher']
        labels = {
            'is_class_teacher': 'Profesor Prinsipal',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('professor', css_class='col-md-6'),
                Column('ano', css_class='col-md-6'),
            ),
            Row(
                Column('departamento', css_class='col-md-4'),
                Column('classe', css_class='col-md-4'),
                Column('turma', css_class='col-md-4'),
            ),
            Row(
                Column('is_class_teacher', css_class='col-md-6 pt-4'),
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )
