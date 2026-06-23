from .view_ajax import ajax_load_subdistritos, ajax_load_sucos, ajax_load_aldeias

from .view_ano import AnoListView, AnoCreateView, AnoUpdateView, ano_delete_view
from .view_departamento import (
    DepartamentoListView, DepartamentoCreateView, DepartamentoUpdateView, departamento_delete_view,
)
from .view_classe import ClasseListView, ClasseCreateView, ClasseUpdateView, classe_delete_view
from .view_turma import TurmaListView, TurmaCreateView, TurmaUpdateView, turma_delete_view
from .view_periodo import PeriodoListView, PeriodoCreateView, PeriodoUpdateView, periodo_delete_view
from .view_materia import MateriaListView, MateriaCreateView, MateriaUpdateView, materia_delete_view
