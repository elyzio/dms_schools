from django.db import models
# from django.contrib.auth.models import User
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.utils import timezone

# =============================================================================
# GEOGRAPHIC AND ADMINISTRATIVE MODELS
# =============================================================================

class Distrito(models.Model):
    distrito = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.distrito
    
    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distrito"
        ordering = ['distrito']

class Subdistrito(models.Model):
    subdistrito = models.CharField(max_length=100)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, related_name='subdistritos')
    
    def __str__(self):
        return f"{self.subdistrito} ({self.distrito.distrito})"
    
    class Meta:
        verbose_name = "Subdistrito"
        verbose_name_plural = "Subdistrito"
        ordering = ['distrito__distrito', 'subdistrito']
        unique_together = ['subdistrito', 'distrito']

class Suco(models.Model):
    suco = models.CharField(max_length=100)
    subdistrito = models.ForeignKey(Subdistrito, on_delete=models.CASCADE, related_name='sucos')
    
    def __str__(self):
        return f"{self.suco} ({self.subdistrito.subdistrito})"
    
    class Meta:
        verbose_name = "Suco"
        verbose_name_plural = "Suco"
        ordering = ['subdistrito__subdistrito', 'suco']
        unique_together = ['suco', 'subdistrito']

class Aldeia(models.Model):
    aldeia = models.CharField(max_length=100)
    suco = models.ForeignKey(Suco, on_delete=models.CASCADE, related_name='aldeias')
    
    def __str__(self):
        return f"{self.aldeia} ({self.suco.suco})"
    
    class Meta:
        verbose_name = "Aldeia"
        verbose_name_plural = "Aldeia"
        ordering = ['suco__suco', 'aldeia']
        unique_together = ['aldeia', 'suco']

# =============================================================================
# ACADEMIC STRUCTURE MODELS
# =============================================================================

class Ano(models.Model):
    ano = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.ano}"
    
    class Meta:
        verbose_name = "Ano Akademiku"
        verbose_name_plural = "Ano Akademiku"
        ordering = ['-ano']
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one active year
            Ano.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class Departamento(models.Model):
    departamento = models.CharField(max_length=100, unique=True)
    sigla = models.CharField(max_length=10, null=True, blank=True, unique=True, help_text="Abbreviation")
    
    def __str__(self):
        return self.departamento
    
    class Meta:
        verbose_name = "Departmentu"
        verbose_name_plural = "Departmentu"
        ordering = ['departamento']

class Classe(models.Model):
    classe = models.CharField(max_length=50, unique=True)  # e.g., "Grade 7", "Class 10A"
    
    def __str__(self):
        return self.classe
    
    class Meta:
        verbose_name = "Klase"
        verbose_name_plural = "Klase"
        ordering = ['classe']

class Turma(models.Model):
    turma = models.CharField(max_length=50, unique=True)  # e.g., "A", "B", "C"
    
    def __str__(self):
        return self.turma
    
    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turma"
        ordering = ['turma']

class Periodo(models.Model):
    periodo = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField()
    
    def __str__(self):
        return self.periodo
    
    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodo"
        ordering = ['periodo']
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one active year
            Periodo.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class Materia(models.Model):
    materia = models.CharField(max_length=100)
    departamentu = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    codigo = models.CharField(max_length=20, unique=True, help_text="Codigo Materia")
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.materia}"
    
    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materia"
        ordering = ['codigo']