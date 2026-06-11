from custom.models import Ano
from .models import Horariu


def professor_horariu(request):
    """
    Injects `teacher_horariu_professor_pk` for teachers who have at least one
    active schedule entry in the current active academic year.
    Returns empty dict for all other users.
    """
    if not request.user.is_authenticated:
        return {}
    if not request.user.groups.filter(name='professor').exists():
        return {}
    try:
        professor = request.user.professoruser.professor
    except Exception:
        return {}
    try:
        active_year = Ano.objects.get(is_active=True)
    except Ano.DoesNotExist:
        return {}
    has_horariu = Horariu.objects.filter(
        professor_materia__professor=professor,
        ano_academico=active_year,
        is_active=True,
    ).exists()
    if has_horariu:
        return {'teacher_horariu_professor_pk': professor.pk}
    return {}
