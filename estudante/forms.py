from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, HTML, Fieldset
from custom.models import Ano
from .models import Estudante, EstudanteClasse, EstudanteTransfer


class EstudanteForm(forms.ModelForm):
    class Meta:
        model = Estudante
        fields = [
            'numero_estudante', 'emis', 'nome', 'sexu',
            'data_moris', 'fatin_moris', 'nacionalidade',
            'distrito', 'subdistrito', 'suco', 'aldeia',
            'kontatu', 'hela_fatin',
            'is_active', 'is_transfer', 'data_matricula',
            'imagem',
        ]
        widgets = {
            'data_moris': forms.DateInput(attrs={'type': 'date'}),
            'data_matricula': forms.DateInput(attrs={'type': 'date'}),
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
                    Column('data_moris', css_class='col-md-3'),
                ),
                Row(
                    Column('fatin_moris', css_class='col-md-6'),
                    Column('nacionalidade', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Rejistu EMIS',
                Row(
                    Column('numero_estudante', css_class='col-md-6'),
                    Column('emis', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Enderesu',
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
                    Column('hela_fatin', css_class='col-md-8'),
                ),
            ),
            Fieldset(
                'Estadu',
                Row(
                    Column('is_active', css_class='col-md-4'),
                    Column('is_transfer', css_class='col-md-4'),
                    Column('data_matricula', css_class='col-md-4'),
                ),
            ),
            Fieldset(
                'Foto',
                'imagem',
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class EstudanteClasseForm(forms.ModelForm):
    class Meta:
        model = EstudanteClasse
        fields = [
            'ano', 'departamentu', 'classe', 'turma',
            'data_enrollment', 'is_mid_year_transfer', 'starting_period',
        ]
        widgets = {
            'data_enrollment': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            active_year = Ano.objects.get(is_active=True)
            self.fields['ano'].initial = active_year
            self.fields['ano'].disabled = True
        except Ano.DoesNotExist:
            pass
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('ano', css_class='col-md-6'),
                Column('departamentu', css_class='col-md-6'),
            ),
            Row(
                Column('classe', css_class='col-md-6'),
                Column('turma', css_class='col-md-6'),
            ),
            Row(
                Column('data_enrollment', css_class='col-md-4'),
                Column('starting_period', css_class='col-md-4'),
                Column('is_mid_year_transfer', css_class='col-md-4'),
            ),
            Submit('submit', 'Matrikula', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )


class EstudanteTransferForm(forms.ModelForm):
    class Meta:
        model = EstudanteTransfer
        fields = [
            'tipo', 'from_eskola', 'ba_eskola',
            'data_transfer', 'data_aseita', 'obs',
        ]
        widgets = {
            'data_transfer': forms.DateInput(attrs={'type': 'date'}),
            'data_aseita': forms.DateInput(attrs={'type': 'date'}),
            'obs': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('tipo', css_class='col-md-4'),
                Column('data_transfer', css_class='col-md-4'),
                Column('data_aseita', css_class='col-md-4'),
            ),
            Row(
                Column('from_eskola', css_class='col-md-6'),
                Column('ba_eskola', css_class='col-md-6'),
            ),
            'obs',
            Submit('submit', 'Rejista Transferénsia', css_class='btn btn-primary'),
            HTML('<a href="javascript:history.back()" class="btn btn-outline-secondary ms-2">Kansela</a>'),
        )
