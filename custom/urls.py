from django.urls import path
from . import views

urlpatterns = [
    # AJAX (geographic cascade)
    path('ajax/subdistritos/', views.ajax_load_subdistritos, name='ajax-load-subdistritos'),
    path('ajax/sucos/', views.ajax_load_sucos, name='ajax-load-sucos'),
    path('ajax/aldeias/', views.ajax_load_aldeias, name='ajax-load-aldeias'),

    # Ano
    path('ano/', views.AnoListView.as_view(), name='ano-list'),
    path('ano/criar/', views.AnoCreateView.as_view(), name='ano-create'),
    path('ano/<int:pk>/editar/', views.AnoUpdateView.as_view(), name='ano-update'),
    path('ano/<int:pk>/eliminar/', views.ano_delete_view, name='ano-delete'),

    # Departamento
    path('departamento/', views.DepartamentoListView.as_view(), name='departamento-list'),
    path('departamento/criar/', views.DepartamentoCreateView.as_view(), name='departamento-create'),
    path('departamento/<int:pk>/editar/', views.DepartamentoUpdateView.as_view(), name='departamento-update'),
    path('departamento/<int:pk>/eliminar/', views.departamento_delete_view, name='departamento-delete'),

    # Classe
    path('classe/', views.ClasseListView.as_view(), name='classe-list'),
    path('classe/criar/', views.ClasseCreateView.as_view(), name='classe-create'),
    path('classe/<int:pk>/editar/', views.ClasseUpdateView.as_view(), name='classe-update'),
    path('classe/<int:pk>/eliminar/', views.classe_delete_view, name='classe-delete'),

    # Turma
    path('turma/', views.TurmaListView.as_view(), name='turma-list'),
    path('turma/criar/', views.TurmaCreateView.as_view(), name='turma-create'),
    path('turma/<int:pk>/editar/', views.TurmaUpdateView.as_view(), name='turma-update'),
    path('turma/<int:pk>/eliminar/', views.turma_delete_view, name='turma-delete'),

    # Periodo
    path('periodo/', views.PeriodoListView.as_view(), name='periodo-list'),
    path('periodo/criar/', views.PeriodoCreateView.as_view(), name='periodo-create'),
    path('periodo/<int:pk>/editar/', views.PeriodoUpdateView.as_view(), name='periodo-update'),
    path('periodo/<int:pk>/eliminar/', views.periodo_delete_view, name='periodo-delete'),

    # Materia
    path('materia/', views.MateriaListView.as_view(), name='materia-list'),
    path('materia/criar/', views.MateriaCreateView.as_view(), name='materia-create'),
    path('materia/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia-update'),
    path('materia/<int:pk>/eliminar/', views.materia_delete_view, name='materia-delete'),
]
