from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q, Prefetch
from django.utils import timezone
from custom.models import Departamento, Classe, Turma, Distrito, Ano
from main.mixins import admin_required, not_teacher_required, teacher_required
from funcionario.models import ProfessorClasse
from .models import Estudante, EstudanteClasse, EstudanteTransfer, EstudanteAlumni
from .forms import EstudanteForm, EstudanteClasseForm, EstudanteTransferForm


@not_teacher_required
def estudante_list_view(request):
    qs = Estudante.objects.filter(is_delete=False, is_active=True)
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(nome__icontains=q) | Q(emis__icontains=q))

    # Matrikula filter scoped to the active academic year only
    matrikula = request.GET.get('matrikula', '').strip()
    if matrikula == 'yes':
        qs = qs.filter(estudanteclasse__ano__is_active=True)
    elif matrikula == 'no':
        qs = qs.exclude(estudanteclasse__ano__is_active=True)

    # Departamento/classe/turma filters all scoped to the active year (one join)
    matrikula_lookup = {}
    departamentu = request.GET.get('departamentu', '').strip()
    if departamentu:
        matrikula_lookup['estudanteclasse__departamentu_id'] = departamentu
    classe = request.GET.get('classe', '').strip()
    if classe:
        matrikula_lookup['estudanteclasse__classe_id'] = classe
    turma = request.GET.get('turma', '').strip()
    if turma:
        matrikula_lookup['estudanteclasse__turma_id'] = turma
    if matrikula_lookup:
        matrikula_lookup['estudanteclasse__ano__is_active'] = True
        qs = qs.filter(**matrikula_lookup)

    distrito = request.GET.get('distrito', '').strip()
    if distrito:
        qs = qs.filter(distrito_id=distrito)

    # Attach each student's current-year enrollment as a single-item list
    current_year_prefetch = Prefetch(
        'estudanteclasse_set',
        queryset=EstudanteClasse.objects.filter(
            ano__is_active=True
        ).select_related('departamentu', 'classe', 'turma'),
        to_attr='current_matricula',
    )
    qs = qs.prefetch_related(current_year_prefetch)

    return render(request, 'estudante/estudante/list.html', {
        'estudantes': qs.distinct(),
        'q': q,
        'matrikula': matrikula,
        'departamentu_filter': departamentu,
        'classe_filter': classe,
        'turma_filter': turma,
        'distrito_filter': distrito,
        'departamentu_list': Departamento.objects.all(),
        'classe_list': Classe.objects.all(),
        'turma_list': Turma.objects.all(),
        'distrito_list': Distrito.objects.all(),
        'has_filters': any([q, matrikula, departamentu, classe, turma, distrito]),
    })


@not_teacher_required
def estudante_detail_view(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    ec_base = estudante.estudanteclasse_set.select_related('ano', 'departamentu', 'classe', 'turma')
    return render(request, 'estudante/estudante/detail.html', {
        'estudante': estudante,
        'current_matricula': ec_base.filter(ano__is_active=True).first(),
        'classes': ec_base.exclude(ano__is_active=True).order_by('-ano__ano'),
        'transfers': estudante.estudantetransfer_set.order_by('-data_transfer'),
    })


@admin_required
def estudante_create_view(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST, request.FILES)
        if form.is_valid():
            estudante = form.save()
            messages.success(request, f'Estudante {estudante.nome} rejistadu ho susesu.')
            return redirect('estudante-detail', pk=estudante.pk)
    else:
        form = EstudanteForm()
    return render(request, 'estudante/estudante/form.html', {'form': form, 'object': None})


@admin_required
def estudante_update_view(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        form = EstudanteForm(request.POST, request.FILES, instance=estudante)
        if form.is_valid():
            estudante = form.save()
            messages.success(request, f'Dados {estudante.nome} atualiza ho susesu.')
            return redirect('estudante-detail', pk=estudante.pk)
    else:
        form = EstudanteForm(instance=estudante)
    return render(request, 'estudante/estudante/form.html', {'form': form, 'object': estudante})


@admin_required
def estudante_delete_view(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        estudante.is_delete = True
        estudante.is_active = False
        estudante.save()
        messages.warning(request, f'Estudante {estudante.nome} hamoos ona husi sistema.')
        return redirect('estudante-list')
    return redirect('estudante-detail', pk=pk)


@admin_required
def estudante_matricula_create_view(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        form = EstudanteClasseForm(request.POST)
        if form.is_valid():
            form.instance.estudante = estudante
            form.save()
            messages.success(request, 'Matrikula rejistadu ho susesu.')
            return redirect('estudante-detail', pk=pk)
    else:
        initial = {
            k: v for k, v in request.GET.items()
            if k in ('classe', 'departamentu', 'turma') and v
        }
        form = EstudanteClasseForm(initial=initial)
    return render(request, 'estudante/estudanteClasse/form.html', {'form': form, 'estudante': estudante})


@admin_required
def estudante_transfer_create_view(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        form = EstudanteTransferForm(request.POST)
        if form.is_valid():
            form.instance.estudante = estudante
            form.save()
            estudante.is_transfer = True
            if form.instance.tipo == 'OUT':
                estudante.is_active = False
            estudante.save(update_fields=['is_transfer', 'is_active'])
            messages.success(request, 'Transferénsia rejistadu ho susesu.')
            return redirect('estudante-detail', pk=pk)
    else:
        form = EstudanteTransferForm()
    return render(request, 'estudante/estudanteTransfer/form.html', {'form': form, 'estudante': estudante})


# =============================================================================
# ESTUDANTE PASSA (Promotion)
# =============================================================================

@admin_required
def estudante_passa_view(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        cm = estudante.estudanteclasse_set.filter(ano__is_active=True).first()
        if cm:
            cm.is_passa = True
            cm.save(update_fields=['is_passa'])
            messages.success(request, f'{estudante.nome} marka ona "Passa" ba tinan ne\'e.')
        else:
            messages.error(request, f'{estudante.nome} seidauk iha matrikula ba ano atuál.')
    return redirect('estudante-passa-list')


@not_teacher_required
def estudante_passa_list_view(request):
    passados = EstudanteClasse.objects.filter(
        ano__is_active=True, is_passa=True,
    ).select_related('estudante', 'classe', 'turma', 'departamentu').order_by(
        'classe__classe', 'turma__turma', 'estudante__nome'
    )
    return render(request, 'estudante/estudantePassa/list.html', {'passados': passados})


# =============================================================================
# REINSKRISAUN ESTUDANTE (Re-enrollment)
# =============================================================================

@not_teacher_required
def estudante_reinskrisaun_list_view(request):
    active_ano = Ano.objects.filter(is_active=True).first()
    last_ano = None
    if active_ano:
        last_ano = Ano.objects.filter(
            is_active=False, ano__lt=active_ano.ano,
        ).order_by('-ano').first()

    candidates = []
    if active_ano and last_ano:
        classe_order = list(Classe.objects.order_by('classe'))
        next_classe_map = {
            classe_order[i].id: classe_order[i + 1]
            for i in range(len(classe_order) - 1)
        }
        candidates = list(EstudanteClasse.objects.filter(
            ano=last_ano, estudante__is_active=True, estudante__is_delete=False,
        ).exclude(
            estudante__estudanteclasse__ano=active_ano,
        ).select_related('estudante', 'classe', 'turma', 'departamentu').order_by(
            'classe__classe', 'turma__turma', 'estudante__nome'
        ))
        for ec in candidates:
            if ec.is_passa:
                # passed -> advance to next grade; None if already at the final grade (-> alumni)
                ec.suggested_classe = next_classe_map.get(ec.classe_id)
            else:
                # not passed (False/None) -> repeat the same grade
                ec.suggested_classe = ec.classe

    return render(request, 'estudante/estudanteReinskrisaun/list.html', {
        'candidates': candidates,
        'active_ano': active_ano,
        'last_ano': last_ano,
    })


# =============================================================================
# ALUMNI (Graduation)
# =============================================================================

@not_teacher_required
def estudante_alumni_candidates_view(request):
    candidates = EstudanteClasse.objects.filter(
        ano__is_active=True, classe__classe__startswith='12',
        is_passa=True, estudante__is_alumni=False, estudante__is_active=True,
    ).select_related('estudante', 'classe', 'turma', 'departamentu').order_by(
        'turma__turma', 'estudante__nome'
    )
    return render(request, 'estudante/estudanteAlumni/candidates.html', {'candidates': candidates})


@admin_required
def estudante_alumni_create_view(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        active_ano = Ano.objects.filter(is_active=True).first()
        EstudanteAlumni.objects.create(
            estudante=estudante, data_alumni=timezone.now().date(), ano=active_ano,
        )
        estudante.is_alumni = True
        estudante.is_active = False
        estudante.save(update_fields=['is_alumni', 'is_active'])
        messages.success(request, f'{estudante.nome} hatama ona ba Alumni.')
    return redirect('estudante-alumni-candidates')


@not_teacher_required
def estudante_alumni_list_view(request):
    qs = EstudanteAlumni.objects.select_related('estudante', 'ano')

    ano_filter = request.GET.get('ano', '').strip()
    if ano_filter:
        qs = qs.filter(ano_id=ano_filter)

    departamentu_filter = request.GET.get('departamentu', '').strip()
    if departamentu_filter:
        qs = qs.filter(
            estudante__estudanteclasse__departamentu_id=departamentu_filter,
            estudante__estudanteclasse__classe__classe__startswith='12',
        ).distinct()

    alumni_list = list(qs.order_by('-ano__ano', 'estudante__nome'))

    # Attach each alumni's grade-12 departamentu (the one they graduated from) for display
    estudante_ids = [a.estudante_id for a in alumni_list]
    grad_classes = EstudanteClasse.objects.filter(
        estudante_id__in=estudante_ids, classe__classe__startswith='12',
    ).select_related('departamentu')
    dep_map = {}
    for c in grad_classes:
        dep_map.setdefault(c.estudante_id, {})[c.ano_id] = c.departamentu
    for alum in alumni_list:
        alum.departamentu_display = dep_map.get(alum.estudante_id, {}).get(alum.ano_id)

    return render(request, 'estudante/estudanteAlumni/list.html', {
        'alumni_history': alumni_list,
        'ano_filter': ano_filter,
        'departamentu_filter': departamentu_filter,
        'ano_list': Ano.objects.order_by('-ano'),
        'departamentu_list': Departamento.objects.all(),
    })


# =============================================================================
# ESTUDANTE BA PROFESSOR (Teacher's own class roster — view-only)
# =============================================================================

@teacher_required
def estudante_classe_view(request):
    try:
        professor = request.user.professoruser.professor
    except Exception:
        messages.error(request, 'Perfil professor la hetan.')
        return redirect('dashboard')

    active_ano = Ano.objects.filter(is_active=True).first()
    pairs = []
    if active_ano:
        pairs = list(ProfessorClasse.objects.filter(
            professor=professor, ano=active_ano,
        ).values_list('classe_id', 'turma_id'))

    estudantes = EstudanteClasse.objects.none()
    if pairs:
        q = Q()
        for classe_id, turma_id in pairs:
            q |= Q(classe_id=classe_id, turma_id=turma_id)
        estudantes = EstudanteClasse.objects.filter(q, ano=active_ano).select_related(
            'estudante', 'classe', 'turma', 'departamentu',
        ).order_by('classe__classe', 'turma__turma', 'estudante__nome')

    return render(request, 'estudante/estudanteClasse/professor_list.html', {
        'estudantes': estudantes,
        'has_assignment': bool(pairs),
    })
