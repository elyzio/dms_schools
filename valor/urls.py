from django.urls import path
from .views import (
    valor_materia_list_view, valor_estudante_list_view, valor_input_view,
    valor_estudante_detail_view, valor_delete_view, valor_row_lock_toggle_view,
    valor_lock_bulk_view,
)

urlpatterns = [
    path('', valor_materia_list_view, name='valor-materia-list'),
    path('materia/<int:pm_pk>/', valor_estudante_list_view, name='valor-estudante-list'),
    path('materia/<int:pm_pk>/lock/', valor_lock_bulk_view, name='valor-lock-bulk'),
    path('input/<int:estudante_classe_pk>/<int:materia_pk>/<int:periodo_pk>/', valor_input_view, name='valor-input'),
    path('estudante/<int:estudante_pk>/', valor_estudante_detail_view, name='valor-estudante-detail'),
    path('delete/<int:valor_pk>/', valor_delete_view, name='valor-delete'),
    path('row-lock/<int:valor_pk>/', valor_row_lock_toggle_view, name='valor-row-lock-toggle'),
]
