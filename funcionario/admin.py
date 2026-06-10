from django.contrib import admin
from .models import Professor, ProfessorUser, ProfessorClasse, ProfessorMateria


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero_funcionario', 'posisaun_prof', 'estadu', 'is_active')
    list_filter = ('estadu', 'posisaun_prof', 'is_active', 'sexu', 'nivel_akademiku')
    search_fields = ('nome', 'numero_funcionario', 'emis_prof')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProfessorUser)
class ProfessorUserAdmin(admin.ModelAdmin):
    list_display = ('professor', 'user', 'created_at')
    search_fields = ('professor__nome', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(ProfessorClasse)
class ProfessorClasseAdmin(admin.ModelAdmin):
    list_display = ('professor', 'ano', 'classe', 'turma', 'is_class_teacher')
    list_filter = ('ano', 'classe', 'is_class_teacher')
    search_fields = ('professor__nome',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProfessorMateria)
class ProfessorMateriaAdmin(admin.ModelAdmin):
    list_display = ('professor', 'materia', 'classe', 'is_active')
    list_filter = ('is_active', 'classe')
    search_fields = ('professor__nome', 'materia__materia')
    readonly_fields = ('created_at', 'updated_at')
