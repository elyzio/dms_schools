from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from custom.models import Distrito, Subdistrito, Suco, Aldeia, Ano, Departamento, Classe, Turma
from .utils import img_est, doc_est

# =============================================================================
# ESTUDANTE MODELS
# =============================================================================

class Estudante(models.Model):
    SEXU_CHOICES = [
        ('M', 'Mane'),
        ('F', 'Feto'),
    ]

    numero_estudante = models.CharField(max_length=50)
    emis = models.CharField(max_length=100, unique=True, help_text="ID estudante ka númeru rejistu")
    nome = models.CharField(max_length=255)
    sexu = models.CharField(max_length=1, choices=SEXU_CHOICES)
    data_moris = models.DateField()
    fatin_moris = models.CharField(max_length=255)
    nacionalidade = models.CharField(max_length=100, default='Timorense')

    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
    subdistrito = models.ForeignKey(Subdistrito, on_delete=models.PROTECT)
    suco = models.ForeignKey(Suco, on_delete=models.PROTECT)
    aldeia = models.ForeignKey(Aldeia, on_delete=models.PROTECT)
    
    kontatu = models.CharField(max_length=20,null=True, blank=True)
    hela_fatin = models.CharField(max_length=50, help_text="Enderesu Kompletu", blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_transfer = models.BooleanField(default=False)
    is_alumni = models.BooleanField(default=False)
    data_matricula = models.DateField(blank=True, null=True, help_text="Data Matrikula")
    imagem = models.ImageField(upload_to=img_est, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nome} ({self.emis})"
    
    class Meta:
        verbose_name = "Estudante"
        verbose_name_plural = "Estudante"
        ordering = ['nome']

# class EstudanteUser(models.Model):
#     estudante = models.OneToOneField(Estudante, on_delete=models.CASCADE)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.estudante.nome} - {self.user.username}"

class EstudanteClasse(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE)
    departamentu = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    is_passa = models.BooleanField(null=True, blank=True, help_text="Estudante ne'e liu ona klase ida-ne'e?")
    average_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Média Jeral")
    kompensasaun_atitude = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(2)], help_text="Kompensasaun husi atitude (0-2 pontos)")
    kompensasaun_aprova = models.BooleanField(default=False, help_text="Aprova ho kompensasaun?")
    obs_passa = models.TextField(blank=True, help_text="Observasaun kona-ba aprovasaun")
    data_enrollment = models.DateField(default=timezone.now)
    is_mid_year_transfer = models.BooleanField(default=False, help_text="Estudante transfere iha klaran tinan?")
    starting_period = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)], help_text="Período ne'ebé estudante hahu inskrisaun (1=P1, 2=P2, 3=P3)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.estudante.nome} - {self.classe.classe}{self.turma.turma} ({self.ano.ano})"

    class Meta:
        unique_together = ['estudante', 'ano', 'classe', 'turma']
        verbose_name = "Estudante"
        verbose_name_plural = "Estudante"

class EstudanteTransfer(models.Model):
    TIPO_CHOICES = [
        ('IN', 'Transfere Tama'),
        ('OUT', 'Tranfere Sai'),
    ]
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    from_eskola = models.CharField(max_length=255, help_text="Eskola Anterior")
    ba_eskola = models.CharField(max_length=255, help_text="Eskola Destinasaun")
    data_transfer = models.DateField()
    data_aseita = models.DateField(null=True, blank=True, help_text="Data simu iha eskola foun")
    obs = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.estudante.nome} - Tranfere husi {self.from_eskola} ba {self.ba_eskola}"
    
    class Meta:
        verbose_name = "Transferénsia Estudante"
        verbose_name_plural = "Transferénsia Estudante"
        ordering = ['-data_transfer']

class EstudanteAlumni(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    data_alumni = models.DateField()
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, help_text="Tinan graduasaun")
    obs = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.estudante.nome} - Alumni {self.ano.ano}"
    
    class Meta:
        verbose_name = "Alumni"
        verbose_name_plural = "Alumni"
        ordering = ['-data_alumni']

# class EstudanteEncarregadu(models.Model):
#     RELASAUN_CHOICES = [
#         ('PAI', 'Pai'),
#         ('MAE', 'Mãe'),
#         ('AVO', 'Avô/Avó'),
#         ('TIO', 'Tio/Tia'),
#         ('IRMAO', 'Irmão/Irmã'),
#         ('TUTOR', 'Tutor'),
#         ('OUTRO', 'Outro'),
#     ]
    
#     estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
#     encarregadu = models.CharField(max_length=255, help_text="Naran Encaregadu Edukasaun")
#     no_kontatu = models.CharField(max_length=20)
#     email = models.EmailField(blank=True)
#     relasaun = models.CharField(max_length=20, choices=RELASAUN_CHOICES)
#     is_primary = models.BooleanField(default=False, help_text="Ida-ne'e maka Enkaregadu Edukasaun prinsipál?")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.encarregadu} - {self.estudante.nome} ({self.get_relasaun_display()})"
    
#     class Meta:
#         verbose_name = "Encaregadu Edukasaun Estudante"
#         verbose_name_plural = "Encaregadu Edukasaun Estudante"

# class EstudanteDokumentu(models.Model):
#     TIPO_DOKUMENTU_CHOICES = [
#         ('RDTL', 'RDTL'),
#         ('BAPTISMU', 'BAPTISMU'),
#         ('DIPLOMA_3CICLO', 'DIPLOMA 3º CICLO'),
#         ('OUTRO', 'OUTRO'),
#     ]
    
#     estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
#     tipo_dokumentu = models.CharField(max_length=20, choices=TIPO_DOKUMENTU_CHOICES)
#     file = models.FileField(upload_to=doc_est, null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
#     obs = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.estudante.nome} - {self.get_tipo_dokumentu_display()}"

#     class Meta:
#         verbose_name = "Dokumentu Estudante"
#         verbose_name_plural = "Dokumentu Estudante"
#         unique_together = ['tipo_dokumentu', 'estudante']