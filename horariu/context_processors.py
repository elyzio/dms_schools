def professor_horariu(request):
    """
    Injects `teacher_horariu_professor_pk` for any teacher who has a linked
    Professor record, so the Horariu menu link is always visible.
    The view itself handles the empty-schedule case.
    """
    if not request.user.is_authenticated:
        return {}
    if not request.user.groups.filter(name='professor').exists():
        return {}
    try:
        return {'teacher_horariu_professor_pk': request.user.professoruser.professor.pk}
    except Exception:
        return {}
