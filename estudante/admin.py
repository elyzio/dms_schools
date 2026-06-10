from django.contrib import admin
from .models import Estudante, EstudanteClasse, EstudanteTransfer, EstudanteAlumni


@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'emis', 'sexu', 'is_active', 'is_transfer', 'is_alumni')
    list_filter = ('sexu', 'is_active', 'is_transfer', 'is_alumni', 'is_delete')
    search_fields = ('nome', 'emis', 'numero_estudante')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EstudanteClasse)
class EstudanteClasseAdmin(admin.ModelAdmin):
    list_display = ('estudante', 'ano', 'classe', 'turma', 'is_passa')
    list_filter = ('ano', 'classe', 'turma', 'is_passa')
    search_fields = ('estudante__nome', 'estudante__emis')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EstudanteTransfer)
class EstudanteTransferAdmin(admin.ModelAdmin):
    list_display = ('estudante', 'tipo', 'from_eskola', 'ba_eskola', 'data_transfer')
    list_filter = ('tipo',)
    search_fields = ('estudante__nome',)
    readonly_fields = ('created_at',)


@admin.register(EstudanteAlumni)
class EstudanteAlumniAdmin(admin.ModelAdmin):
    list_display = ('estudante', 'ano', 'data_alumni')
    list_filter = ('ano',)
    search_fields = ('estudante__nome',)
    readonly_fields = ('created_at',)
