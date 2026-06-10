from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from custom.models import Ano, Departamento, Classe, Turma, Materia, Distrito, Subdistrito, Suco, Aldeia
from .utils import *

# =============================================================================
# PROFESSOR MODELS
# =============================================================================

class Professor(models.Model):
    STATUS_CHOICES = [
        ('KONTRATADU', 'Kontratadu'),
        ('PERMANENTE', 'Permanente'),
        ('VOLUNTARIU', 'Voluntariu'),
        ('PARCIAL', 'Parcial'),
    ]

    CIVIL_STATUS_CHOICES = [
        ('SOLTEIRO', 'Solteiru/a'),
        ('CASADO', 'Casadu/a'),
        ('BARLAKEADU', 'Barlakeadu/a'),
    ]

    NIVEL_AKADEMIK = [
        ('D1', 'Diploma 1/D1'),
        ('D2', 'Diploma 2/D2'),
        ('D3', 'Diploma 3/D3'),
        ('S1', 'Licensiatura/S1'),
        ('S2', 'Masteradu/S2'),
        ('S3', 'Doutoramentu/S3'),
        ('Outru', 'Outru'),
    ]

    POSISAUN = [
        ('DIRETOR', 'Diretor/a'),
        ('DIRETOR_ADJUNTO', 'Diretor Adjunto'),
        ('GAT', 'Gabinete Apoio Tecnico (GAT)'),
        ('PROFESSOR', 'Professor/a'),
        ('TECNICO_ADMINISTRAÇÃO', 'Tecnico Administraçãon'),
        ('APOIA_ADMINISTRAÇÃO', 'Apoia Administraçãaun'),
        ('GURDA_ESCOLA', 'Guarda Escola'),
        ('TECNICO_AGUA_SANEAMENTO', 'Tecnico Agua Saneamento'),
        ('JARDINHEIRA', 'Jardinheira'),
    ]

    SEXU_CHOICES = [
        ('M', 'Mane'),
        ('F', 'Feto'),
    ]
    
    nome = models.CharField(max_length=255)
    sexu = models.CharField(max_length=1, choices=SEXU_CHOICES)
    eleitoral_prof = models.CharField(max_length=50)
    emis_prof = models.CharField(max_length=20)
    data_moris = models.DateField()
    fatin_moris = models.CharField(max_length=255)
    nacionalidade = models.CharField(max_length=100, default='Timorense')
    
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
    subdistrito = models.ForeignKey(Subdistrito, on_delete=models.PROTECT)
    suco = models.ForeignKey(Suco, on_delete=models.PROTECT)
    aldeia = models.ForeignKey(Aldeia, on_delete=models.PROTECT)
    kontatu = models.CharField(max_length=20, blank=True)
    hela_fatin = models.CharField(max_length=50 ,help_text="Full address", blank=True, null=True)
    
    estadu = models.CharField(max_length=20, choices=STATUS_CHOICES)
    nivel_akademiku = models.CharField(max_length=100, choices=NIVEL_AKADEMIK)
    grau_akademiku = models.CharField(max_length=100, null=True, blank=True)
    numero_funcionario = models.CharField(max_length=50, unique=True, null=True, blank=True)
    posisaun_prof = models.CharField(max_length=40, null=True, blank=True, choices=POSISAUN)
    data_contratacao = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    estadu_civil = models.CharField(max_length=20, choices=CIVIL_STATUS_CHOICES, blank=True)
    email = models.EmailField(null=True, blank=True)
    imagem = models.ImageField(upload_to=img_prof, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nome} ({self.numero_funcionario})"
    
    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionario"
        ordering = ['nome']

class ProfessorUser(models.Model):
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.professor.nome} - {self.user.username}"

class ProfessorClasse(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    is_class_teacher = models.BooleanField(default=False, help_text="Profesor ida-ne'e maka profesor prinsipal klase nian?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.professor.nome} - {self.classe.classe} ({self.ano.ano})"

    class Meta:
        unique_together = ['professor', 'ano', 'classe', 'turma']

class ProfessorMateria(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.professor.nome} - {self.materia.materia} ({self.classe.classe})"

    class Meta:
        unique_together = ['professor', 'materia', 'classe']
        verbose_name = "Professor da Materia"
        verbose_name_plural = "Professores da Materia"

# class ProfessorDokumentu(models.Model):
#     TIPO_DOKUMENTU_CHOICES = [
#         ('CV', 'Curriculum Vitae'),
#         ('CERTIFICADO', 'Certificado'),
#         ('RDTL', 'RDTL'),
#         ('BAPTISMU', 'Baptismu'),
#         ('DIPLOMA', 'Diploma'),
#         ('OUTRU', 'Outru'),
#     ]
    
#     professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
#     tipo_dokumentu = models.CharField(max_length=20, choices=TIPO_DOKUMENTU_CHOICES)
#     file = models.FileField(upload_to=docs_prof, null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
#     obs = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.professor.nome} - {self.tipo_dokumentu}"
    
#     class Meta:
#         verbose_name = "Dokumentu Professor"
#         verbose_name_plural = "Dokumentus Professores"