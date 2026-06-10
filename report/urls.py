from django.urls import path
from .views import (
    grafiku_view,
    tabela_view,
    report_estudante_list_view,
    report_professor_list_view,
)

urlpatterns = [
    path('grafiku/', grafiku_view, name='report-grafiku'),
    path('tabela/', tabela_view, name='report-tabela'),
    path('estudante/', report_estudante_list_view, name='report-estudante-list'),
    path('professor/', report_professor_list_view, name='report-professor-list'),
]
