from django.contrib import admin
from .models import (
    Distrito, Subdistrito, Suco, Aldeia,
    Ano, Departamento, Classe, Turma, Periodo, Materia,
)


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ('distrito',)
    search_fields = ('distrito',)


@admin.register(Subdistrito)
class SubdistritoAdmin(admin.ModelAdmin):
    list_display = ('subdistrito', 'distrito')
    list_filter = ('distrito',)
    search_fields = ('subdistrito',)


@admin.register(Suco)
class SucoAdmin(admin.ModelAdmin):
    list_display = ('suco', 'subdistrito')
    list_filter = ('subdistrito__distrito',)
    search_fields = ('suco',)


@admin.register(Aldeia)
class AldeiaAdmin(admin.ModelAdmin):
    list_display = ('aldeia', 'suco')
    list_filter = ('suco__subdistrito__distrito',)
    search_fields = ('aldeia',)


@admin.register(Ano)
class AnoAdmin(admin.ModelAdmin):
    list_display = ('ano', 'is_active')
    list_filter = ('is_active',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'sigla')
    search_fields = ('departamento', 'sigla')


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('classe',)
    search_fields = ('classe',)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('turma',)
    search_fields = ('turma',)


@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('periodo', 'is_active')
    list_filter = ('is_active',)


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'materia', 'departamentu')
    list_filter = ('departamentu',)
    search_fields = ('codigo', 'materia')
