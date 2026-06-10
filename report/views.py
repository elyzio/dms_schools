import json
from django.shortcuts import render
from django.db.models import Prefetch
from main.mixins import not_teacher_required

from estudante.models import Estudante, EstudanteClasse
from funcionario.models import Professor
from custom.models import Ano, Distrito, Classe, Turma

from .charts import (
    get_students_by_sex,
    get_teachers_by_sex,
    get_students_by_status,
    get_teachers_by_estadu,
    get_teachers_by_nivel,
    get_students_by_district_chart,
)
from .tables import (
    get_students_by_district_table,
    get_students_by_classe_turma_table,
    get_teachers_by_posisaun_table,
    get_teachers_by_estadu_table,
)


@not_teacher_required
def grafiku_view(request):
    context = {
        'students_by_sex': json.dumps(get_students_by_sex()),
        'teachers_by_sex': json.dumps(get_teachers_by_sex()),
        'students_by_status': json.dumps(get_students_by_status()),
        'teachers_by_estadu': json.dumps(get_teachers_by_estadu()),
        'teachers_by_nivel': json.dumps(get_teachers_by_nivel()),
        'students_by_district': json.dumps(get_students_by_district_chart()),
    }
    return render(request, 'report/grafiku.html', context)


@not_teacher_required
def tabela_view(request):
    district_table = get_students_by_district_table()
    district_total = sum(d['total'] for d in district_table)
    teachers_estadu, teachers_total = get_teachers_by_estadu_table()
    context = {
        'students_by_district': district_table,
        'district_total': district_total,
        'students_by_classe_turma': get_students_by_classe_turma_table(),
        'teachers_by_posisaun': get_teachers_by_posisaun_table(),
        'teachers_by_estadu': teachers_estadu,
        'teachers_total': teachers_total,
    }
    return render(request, 'report/tabela.html', context)


def _get_active_enrollment_prefetch():
    try:
        ano_aktivo = Ano.objects.get(is_active=True)
        qs = EstudanteClasse.objects.filter(ano=ano_aktivo).select_related('classe', 'turma', 'departamentu')
        return ano_aktivo, qs
    except Ano.DoesNotExist:
        return None, EstudanteClasse.objects.none()


@not_teacher_required
def report_estudante_list_view(request):
    qs = Estudante.objects.filter(is_active=True, is_delete=False).select_related('distrito')

    distrito = request.GET.get('distrito', '').strip()
    sexu = request.GET.get('sexu', '').strip()
    classe = request.GET.get('classe', '').strip()
    turma = request.GET.get('turma', '').strip()

    if distrito:
        qs = qs.filter(distrito_id=distrito)
    if sexu:
        qs = qs.filter(sexu=sexu)

    matrikula_lookup = {}
    if classe:
        matrikula_lookup['estudanteclasse__classe_id'] = classe
    if turma:
        matrikula_lookup['estudanteclasse__turma_id'] = turma
    if matrikula_lookup:
        qs = qs.filter(**matrikula_lookup)

    ano_aktivo, enrollment_qs = _get_active_enrollment_prefetch()
    qs = qs.prefetch_related(
        Prefetch('estudanteclasse_set', queryset=enrollment_qs, to_attr='current_enrollment')
    ).distinct()

    context = {
        'estudantes': qs,
        'distrito_list': Distrito.objects.all(),
        'classe_list': Classe.objects.all(),
        'turma_list': Turma.objects.all(),
        'distrito_filter': distrito,
        'sexu_filter': sexu,
        'classe_filter': classe,
        'turma_filter': turma,
        'ano_aktivo': ano_aktivo,
        'has_filters': any([distrito, sexu, classe, turma]),
    }
    return render(request, 'report/estudante_list.html', context)


@not_teacher_required
def report_professor_list_view(request):
    qs = Professor.objects.filter(is_active=True, is_delete=False).select_related('distrito')

    sexu = request.GET.get('sexu', '').strip()
    estadu = request.GET.get('estadu', '').strip()
    posisaun = request.GET.get('posisaun', '').strip()
    nivel = request.GET.get('nivel', '').strip()

    if sexu:
        qs = qs.filter(sexu=sexu)
    if estadu:
        qs = qs.filter(estadu=estadu)
    if posisaun:
        qs = qs.filter(posisaun_prof=posisaun)
    if nivel:
        qs = qs.filter(nivel_akademiku=nivel)

    context = {
        'professores': qs,
        'status_choices': Professor.STATUS_CHOICES,
        'nivel_choices': Professor.NIVEL_AKADEMIK,
        'posisaun_choices': Professor.POSISAUN,
        'sexu_filter': sexu,
        'estadu_filter': estadu,
        'posisaun_filter': posisaun,
        'nivel_filter': nivel,
        'has_filters': any([sexu, estadu, posisaun, nivel]),
    }
    return render(request, 'report/professor_list.html', context)
