import json

from django.contrib import messages
from django.db.models import Sum, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from main.mixins import (
    not_teacher_required, admin_required, teacher_or_admin_required, _is_admin,
)
from custom.models import Ano, Periodo, Materia
from estudante.models import Estudante, EstudanteClasse
from funcionario.models import ProfessorMateria

from .models import Valor
from .forms import ValorForm
from .utils import valor_extenso
from .services import valor_completion_status, required_materias_for


def _get_professor(request):
    try:
        return request.user.professoruser.professor
    except Exception:
        return None


# =============================================================================
# PROFESSOR INPUT FLOW (also reachable by Admin, for overrides)
# =============================================================================

@teacher_or_admin_required
def valor_materia_list_view(request):
    is_admin_user = _is_admin(request.user)

    if is_admin_user:
        materias = ProfessorMateria.objects.filter(
            is_active=True,
        ).select_related('professor', 'materia', 'classe').order_by('classe__classe', 'materia__codigo')
    else:
        professor = _get_professor(request)
        if not professor:
            messages.error(request, 'Perfil professor la hetan.')
            return redirect('dashboard')
        materias = ProfessorMateria.objects.filter(
            professor=professor, is_active=True,
        ).select_related('materia', 'classe').order_by('classe__classe', 'materia__codigo')

    return render(request, 'valor/materia_list.html', {
        'materias': materias, 'is_admin_view': is_admin_user,
    })


@teacher_or_admin_required
def valor_estudante_list_view(request, pm_pk):
    is_admin_user = _is_admin(request.user)

    if is_admin_user:
        pm = get_object_or_404(ProfessorMateria, pk=pm_pk, is_active=True)
    else:
        professor = _get_professor(request)
        if not professor:
            messages.error(request, 'Perfil professor la hetan.')
            return redirect('dashboard')
        pm = get_object_or_404(ProfessorMateria, pk=pm_pk, professor=professor, is_active=True)

    active_ano = Ano.objects.filter(is_active=True).first()

    periodo = None
    periodo_id = request.GET.get('periodo', '').strip()
    if periodo_id:
        periodo = Periodo.objects.filter(pk=periodo_id).first()
    if not periodo:
        periodo = Periodo.objects.filter(is_active=True).first()

    estudantes = []
    if active_ano:
        qs = EstudanteClasse.objects.filter(ano=active_ano, classe=pm.classe)
        if pm.materia.departamentu_id:
            qs = qs.filter(departamentu_id=pm.materia.departamentu_id)
        estudantes = list(qs.select_related('estudante', 'turma', 'departamentu').order_by(
            'turma__turma', 'estudante__nome'
        ))

        if periodo and estudantes:
            existing = {
                v.estudante_classe_id: v
                for v in Valor.objects.filter(
                    estudante_classe__in=estudantes, periodo=periodo, materia=pm.materia,
                )
            }
            for ec in estudantes:
                ec.valor_atual = existing.get(ec.id)

    return render(request, 'valor/estudante_list.html', {
        'pm': pm,
        'estudantes': estudantes,
        'periodo': periodo,
        'periodo_list': Periodo.objects.order_by('id'),
        'active_ano': active_ano,
        'is_admin_view': is_admin_user,
    })


@teacher_or_admin_required
def valor_input_view(request, estudante_classe_pk, materia_pk, periodo_pk):
    is_admin_user = _is_admin(request.user)

    ec = get_object_or_404(EstudanteClasse, pk=estudante_classe_pk)
    materia = get_object_or_404(Materia, pk=materia_pk)
    periodo = get_object_or_404(Periodo, pk=periodo_pk)

    pm = None
    if not is_admin_user:
        professor = _get_professor(request)
        if not professor:
            messages.error(request, 'Perfil professor la hetan.')
            return redirect('dashboard')
        pm = get_object_or_404(
            ProfessorMateria, professor=professor, materia=materia, classe=ec.classe, is_active=True,
        )

    def _back_redirect():
        if is_admin_user:
            return redirect('valor-estudante-detail', estudante_pk=ec.estudante_id)
        list_url = reverse('valor-estudante-list', kwargs={'pm_pk': pm.pk})
        return redirect(f"{list_url}?periodo={periodo.pk}")

    valor_obj = Valor.objects.filter(estudante_classe=ec, materia=materia, periodo=periodo).first()

    if valor_obj and valor_obj.is_lock:
        messages.error(request, "Valor ne'e lock ona — labele edita.")
        return _back_redirect()

    if request.method == 'POST':
        form = ValorForm(request.POST, instance=valor_obj)
        if form.is_valid():
            form.instance.estudante_classe = ec
            form.instance.materia = materia
            form.instance.periodo = periodo
            form.instance.por_extenso = valor_extenso(form.cleaned_data['valor'])
            form.save()
            messages.success(request, f"Valor ba {ec.estudante.nome} grava ona.")
            return _back_redirect()
    else:
        form = ValorForm(instance=valor_obj)

    return render(request, 'valor/input_form.html', {
        'form': form, 'ec': ec, 'materia': materia, 'periodo': periodo, 'pm': pm,
    })


# =============================================================================
# ADMIN OVERRIDES — delete / lock toggles
# =============================================================================

@admin_required
def valor_delete_view(request, valor_pk):
    valor = get_object_or_404(Valor, pk=valor_pk)
    estudante_pk = valor.estudante_classe.estudante_id
    if request.method == 'POST':
        if valor.is_lock:
            messages.error(request, "Valor ne'e lock ona — labele hamoos.")
        else:
            valor.delete()
            messages.success(request, 'Valor hamoos ona.')
    return redirect('valor-estudante-detail', estudante_pk=estudante_pk)


@admin_required
def valor_row_lock_toggle_view(request, valor_pk):
    valor = get_object_or_404(Valor, pk=valor_pk)
    if request.method == 'POST':
        valor.is_lock = not valor.is_lock
        valor.save(update_fields=['is_lock'])
        messages.success(request, "Valor lock ona." if valor.is_lock else "Valor loke ona.")
    return redirect('valor-estudante-detail', estudante_pk=valor.estudante_classe.estudante_id)


@admin_required
def valor_lock_bulk_view(request, pm_pk):
    pm = get_object_or_404(ProfessorMateria, pk=pm_pk, is_active=True)
    if request.method == 'POST':
        periodo = get_object_or_404(Periodo, pk=request.POST.get('periodo'))
        action = request.POST.get('action')
        qs = Valor.objects.filter(
            materia=pm.materia, estudante_classe__classe=pm.classe, periodo=periodo,
        )
        if action == 'lock':
            updated = qs.update(is_lock=True)
            messages.success(request, f"Valor {updated} lock ona ba {pm.materia} — {periodo.periodo}.")
        elif action == 'unlock':
            updated = qs.update(is_lock=False)
            messages.success(request, f"Valor {updated} loke ona ba {pm.materia} — {periodo.periodo}.")
        list_url = reverse('valor-estudante-list', kwargs={'pm_pk': pm.pk})
        return redirect(f"{list_url}?periodo={periodo.pk}")
    return redirect('valor-estudante-list', pm_pk=pm.pk)


# =============================================================================
# REVIEW FLOW (read-only, from student detail — Admin gets extra action icons)
# =============================================================================

@not_teacher_required
def valor_estudante_detail_view(request, estudante_pk):
    estudante = get_object_or_404(Estudante, pk=estudante_pk)
    classes = estudante.estudanteclasse_set.select_related(
        'ano', 'classe', 'turma', 'departamentu',
    ).order_by('ano__ano')

    periodos = list(Periodo.objects.order_by('id'))
    class_data = []
    for ec in classes:
        materias = list(required_materias_for(ec).order_by('codigo'))
        periodo_tables = []
        chart_labels = []
        chart_averages = []
        for periodo in periodos:
            valores = Valor.objects.filter(estudante_classe=ec, periodo=periodo).select_related('materia')
            agg = valores.aggregate(total=Sum('valor'), media=Avg('valor'))
            valor_map = {v.materia_id: v for v in valores}
            rows = [{'materia': m, 'valor': valor_map.get(m.id)} for m in materias]

            periodo_tables.append({
                'periodo': periodo,
                'rows': rows,
                'total': agg['total'],
                'media': agg['media'],
            })
            chart_labels.append(periodo.periodo)
            chart_averages.append(float(agg['media']) if agg['media'] is not None else 0)

        class_data.append({
            'ec': ec,
            'periodo_tables': periodo_tables,
            'chart': json.dumps({'labels': chart_labels, 'data': chart_averages}),
            'completion': valor_completion_status(ec),
        })

    return render(request, 'valor/estudante_detail.html', {
        'estudante': estudante,
        'class_data': class_data,
    })
