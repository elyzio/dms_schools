from django.urls import path
from .views import (
    HorasListView, HorasCreateView, HorasUpdateView, horas_delete_view,
    HorariuListView, HorariuCreateView, HorariuUpdateView, horariu_delete_view,
    HorariuByTurmaView, HorariuByProfessorView, HorariuHanorinView,
    HorariuMasterTableView,
)

urlpatterns = [
    # Horas (time slots)
    path('horas/', HorasListView.as_view(), name='horas-list'),
    path('horas/criar/', HorasCreateView.as_view(), name='horas-create'),
    path('horas/<int:pk>/editar/', HorasUpdateView.as_view(), name='horas-update'),
    path('horas/<int:pk>/eliminar/', horas_delete_view, name='horas-delete'),

    # Horariu special views (before pk-based patterns)
    path('hanorin/', HorariuHanorinView.as_view(), name='horariu-hanorin'),
    path('tabela/', HorariuMasterTableView.as_view(), name='horariu-master-table'),
    path('turma/<int:classe_pk>/<int:turma_pk>/', HorariuByTurmaView.as_view(), name='horariu-by-turma'),
    path('professor/<int:professor_pk>/', HorariuByProfessorView.as_view(), name='horariu-by-professor'),

    # Horariu CRUD
    path('', HorariuListView.as_view(), name='horariu-list'),
    path('criar/', HorariuCreateView.as_view(), name='horariu-create'),
    path('<int:pk>/editar/', HorariuUpdateView.as_view(), name='horariu-update'),
    path('<int:pk>/eliminar/', horariu_delete_view, name='horariu-delete'),
]
