from django.db.models import Q
from custom.models import Materia, Periodo
from .models import Valor


def required_materias_for(estudante_classe):
    """Materia rows actually taught in this classe, scoped to the student's own department (or general)."""
    return Materia.objects.filter(
        professormateria__classe=estudante_classe.classe,
        professormateria__is_active=True,
    ).filter(
        Q(departamentu__isnull=True) | Q(departamentu=estudante_classe.departamentu)
    ).distinct()


def periods_required_for(estudante_classe):
    """All periods, or only the ones from the student's starting_period onward if they transferred in mid-year."""
    periods = list(Periodo.objects.order_by('id'))
    if estudante_classe.is_mid_year_transfer and estudante_classe.starting_period:
        periods = periods[estudante_classe.starting_period - 1:]
    return periods


def valor_completion_status(estudante_classe):
    materias = list(required_materias_for(estudante_classe))
    periods = periods_required_for(estudante_classe)
    required = len(materias) * len(periods)
    filled = Valor.objects.filter(
        estudante_classe=estudante_classe, materia__in=materias, periodo__in=periods,
    ).count()
    return {
        'required': required,
        'filled': filled,
        'complete': required > 0 and filled >= required,
    }
