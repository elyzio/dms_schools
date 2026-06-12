from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from main.mixins import AdminRequiredMixin, NotTeacherMixin, admin_required
from custom.models import Classe, Turma
from funcionario.models import Professor
from .models import Horas, Horariu
from .forms import HorasForm, HorariuForm


# =============================================================================
# HORAS (Time Slots)
# =============================================================================

class HorasListView(NotTeacherMixin, ListView):
    model = Horas
    template_name = 'horariu/horas/list.html'
    context_object_name = 'horas_list'


class HorasCreateView(AdminRequiredMixin, CreateView):
    model = Horas
    form_class = HorasForm
    template_name = 'horariu/horas/form.html'
    success_url = reverse_lazy('horas-list')

    def form_valid(self, form):
        messages.success(self.request, 'Oras kria ho susesu.')
        return super().form_valid(form)


class HorasUpdateView(AdminRequiredMixin, UpdateView):
    model = Horas
    form_class = HorasForm
    template_name = 'horariu/horas/form.html'
    success_url = reverse_lazy('horas-list')

    def form_valid(self, form):
        messages.success(self.request, 'Oras atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def horas_delete_view(request, pk):
    horas = get_object_or_404(Horas, pk=pk)
    if request.method == 'POST':
        messages.warning(request, f'Oras {horas} hamoos ona.')
        horas.delete()
    return redirect('horas-list')


# =============================================================================
# HORARIU (Schedule)
# =============================================================================

class HorariuListView(NotTeacherMixin, ListView):
    model = Horariu
    template_name = 'horariu/horariu/list.html'
    context_object_name = 'horarios'

    def get_queryset(self):
        qs = Horariu.objects.select_related(
            'horas', 'classe', 'turma', 'departamento',
            'professor_materia__professor', 'professor_materia__materia',
            'ano_academico',
        ).order_by('loron', 'horas__horas_hahu')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(classe__classe__icontains=q) |
                Q(turma__turma__icontains=q) |
                Q(professor_materia__professor__nome__icontains=q) |
                Q(professor_materia__materia__materia__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class HorariuCreateView(AdminRequiredMixin, CreateView):
    model = Horariu
    form_class = HorariuForm
    template_name = 'horariu/horariu/form.html'
    success_url = reverse_lazy('horariu-list')

    def form_valid(self, form):
        messages.success(self.request, 'Horariu kria ho susesu.')
        return super().form_valid(form)


class HorariuUpdateView(AdminRequiredMixin, UpdateView):
    model = Horariu
    form_class = HorariuForm
    template_name = 'horariu/horariu/form.html'
    success_url = reverse_lazy('horariu-list')

    def form_valid(self, form):
        messages.success(self.request, 'Horariu atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def horariu_delete_view(request, pk):
    horariu = get_object_or_404(Horariu, pk=pk)
    if request.method == 'POST':
        messages.warning(request, 'Entrada horariu hamoos ona.')
        horariu.delete()
    return redirect('horariu-list')


# =============================================================================
# SPECIAL VIEWS — grid by turma / by professor
# =============================================================================

def _build_grid(horarios, horas_qs):
    """Build {horas_pk: {loron_code: horariu_obj}} for weekly grid templates."""
    grid = {h.pk: {} for h in horas_qs}
    for horariu in horarios:
        grid.setdefault(horariu.horas_id, {})[horariu.loron] = horariu
    return grid


class HorariuByTurmaView(LoginRequiredMixin, ListView):
    model = Horariu
    template_name = 'horariu/horariu/turma_detail.html'
    context_object_name = 'horarios'

    def get_queryset(self):
        return Horariu.objects.filter(
            classe_id=self.kwargs['classe_pk'],
            turma_id=self.kwargs['turma_pk'],
            is_active=True,
        ).select_related(
            'horas', 'professor_materia__professor', 'professor_materia__materia',
        ).order_by('horas__horas_hahu')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        horas_qs = Horas.objects.all()
        ctx['classe'] = get_object_or_404(Classe, pk=self.kwargs['classe_pk'])
        ctx['turma'] = get_object_or_404(Turma, pk=self.kwargs['turma_pk'])
        ctx['horas_list'] = horas_qs
        ctx['dias'] = Horariu.LORON_CHOICES
        ctx['grid'] = _build_grid(ctx['horarios'], horas_qs)
        return ctx


class HorariuHanorinView(LoginRequiredMixin, ListView):
    """Personal schedule view for the logged-in teacher — no PK in the URL."""
    model = Horariu
    template_name = 'horariu/horariu/professor_detail.html'
    context_object_name = 'horarios'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='professor').exists():
            messages.error(request, 'Asesu la permiti.')
            return redirect('dashboard')
        try:
            self._professor = request.user.professoruser.professor
        except Exception:
            messages.error(request, 'Perfil professor la hetan.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Horariu.objects.filter(
            professor_materia__professor=self._professor,
            is_active=True,
        ).select_related(
            'horas', 'classe', 'turma', 'professor_materia__materia',
        ).order_by('horas__horas_hahu')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        horas_qs = Horas.objects.all()
        ctx['professor'] = self._professor
        ctx['horas_list'] = horas_qs
        ctx['dias'] = Horariu.LORON_CHOICES
        ctx['grid'] = _build_grid(ctx['horarios'], horas_qs)
        return ctx


class HorariuByProfessorView(LoginRequiredMixin, ListView):
    model = Horariu
    template_name = 'horariu/horariu/professor_detail.html'
    context_object_name = 'horarios'

    def get_queryset(self):
        return Horariu.objects.filter(
            professor_materia__professor_id=self.kwargs['professor_pk'],
            is_active=True,
        ).select_related(
            'horas', 'classe', 'turma', 'professor_materia__materia',
        ).order_by('horas__horas_hahu')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        horas_qs = Horas.objects.all()
        ctx['professor'] = get_object_or_404(Professor, pk=self.kwargs['professor_pk'])
        ctx['horas_list'] = horas_qs
        ctx['dias'] = Horariu.LORON_CHOICES
        ctx['grid'] = _build_grid(ctx['horarios'], horas_qs)
        return ctx
