import json

from django.contrib import messages
from django.db.models import Sum, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from main.mixins import teacher_required, not_teacher_required
from custom.models import Ano, Periodo, Materia
from estudante.models import Estudante, EstudanteClasse
from funcionario.models import ProfessorMateria

from .models import Valor
from .forms import ValorForm
from .utils import valor_extenso
from .services import valor_completion_status


def _get_professor(request):
    try:
        return request.user.professoruser.professor
    except Exception:
        return None


# =============================================================================
# PROFESSOR INPUT FLOW
# =============================================================================

@teacher_required
def valor_materia_list_view(request):
    professor = _get_professor(request)
    if not professor:
        messages.error(request, 'Perfil professor la hetan.')
        return redirect('dashboard')

    materias = ProfessorMateria.objects.filter(
        professor=professor, is_active=True,
    ).select_related('materia', 'classe').order_by('classe__classe', 'materia__codigo')

    return render(request, 'valor/materia_list.html', {'materias': materias})


@teacher_required
def valor_estudante_list_view(request, pm_pk):
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
    })


@teacher_required
def valor_input_view(request, estudante_classe_pk, materia_pk, periodo_pk):
    professor = _get_professor(request)
    if not professor:
        messages.error(request, 'Perfil professor la hetan.')
        return redirect('dashboard')

    ec = get_object_or_404(EstudanteClasse, pk=estudante_classe_pk)
    materia = get_object_or_404(Materia, pk=materia_pk)
    periodo = get_object_or_404(Periodo, pk=periodo_pk)
    pm = get_object_or_404(
        ProfessorMateria, professor=professor, materia=materia, classe=ec.classe, is_active=True,
    )

    valor_obj = Valor.objects.filter(estudante_classe=ec, materia=materia, periodo=periodo).first()

    if valor_obj and valor_obj.is_lock:
        messages.error(request, "Valor ne'e selu ona — labele edita.")
        return redirect('valor-estudante-list', pm_pk=pm.pk)

    if request.method == 'POST':
        form = ValorForm(request.POST, instance=valor_obj)
        if form.is_valid():
            form.instance.estudante_classe = ec
            form.instance.materia = materia
            form.instance.periodo = periodo
            form.instance.por_extenso = valor_extenso(form.cleaned_data['valor'])
            form.save()
            messages.success(request, f"Valor ba {ec.estudante.nome} grava ona.")
            list_url = reverse('valor-estudante-list', kwargs={'pm_pk': pm.pk})
            return redirect(f"{list_url}?periodo={periodo.pk}")
    else:
        form = ValorForm(instance=valor_obj)

    return render(request, 'valor/input_form.html', {
        'form': form, 'ec': ec, 'materia': materia, 'periodo': periodo, 'pm': pm,
    })


# =============================================================================
# REVIEW FLOW (read-only, from student detail)
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
        periodo_tables = []
        chart_labels = []
        chart_averages = []
        for periodo in periodos:
            valores = Valor.objects.filter(estudante_classe=ec, periodo=periodo).select_related(
                'materia',
            ).order_by('materia__codigo')
            agg = valores.aggregate(total=Sum('valor'), media=Avg('valor'))
            periodo_tables.append({
                'periodo': periodo,
                'valores': valores,
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
