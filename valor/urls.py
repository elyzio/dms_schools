from django.urls import path
from .views import (
    valor_materia_list_view, valor_estudante_list_view, valor_input_view,
    valor_estudante_detail_view,
)

urlpatterns = [
    path('', valor_materia_list_view, name='valor-materia-list'),
    path('materia/<int:pm_pk>/', valor_estudante_list_view, name='valor-estudante-list'),
    path('input/<int:estudante_classe_pk>/<int:materia_pk>/<int:periodo_pk>/', valor_input_view, name='valor-input'),
    path('estudante/<int:estudante_pk>/', valor_estudante_detail_view, name='valor-estudante-detail'),
]
