from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q
from custom.models import Departamento, Classe, Turma, Distrito
from main.mixins import admin_required, not_teacher_required
from .models import Estudante, EstudanteClasse, EstudanteTransfer
from .forms import EstudanteForm, EstudanteClasseForm, EstudanteTransferForm


@not_teacher_required
def estudante_list_view(request):
    qs = Estudante.objects.filter(is_delete=False)
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(nome__icontains=q) | Q(emis__icontains=q))

    matrikula = request.GET.get('matrikula', '').strip()
    if matrikula == 'yes':
        qs = qs.filter(estudanteclasse__isnull=False)
    elif matrikula == 'no':
        qs = qs.filter(estudanteclasse__isnull=True)

    # Department/classe/turma must match on the same matrikula record,
    # so they're combined into a single filter() call (one join).
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
        qs = qs.filter(**matrikula_lookup)

    distrito = request.GET.get('distrito', '').strip()
    if distrito:
        qs = qs.filter(distrito_id=distrito)

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
    return render(request, 'estudante/estudante/detail.html', {
        'estudante': estudante,
        'classes': estudante.estudanteclasse_set.select_related(
            'ano', 'classe', 'turma'
        ).order_by('-ano__ano'),
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
        form = EstudanteClasseForm()
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
