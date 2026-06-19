from collections import OrderedDict, defaultdict

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from main.mixins import AdminRequiredMixin, NotTeacherMixin, admin_required
from custom.models import Classe, Turma, Materia
from funcionario.models import Professor
from .models import Horas, Horariu
from .forms import HorasForm, HorariuForm

_MASTER_DAYS = [
    ('SEG', 'Segunda-Feira'),
    ('TER', 'Terça-Feira'),
    ('QUA', 'Quarta-Feira'),
    ('QUI', 'Kinta-Feira'),
    ('SEX', 'Sexta-Feira'),
    ('SAB', 'Sábado'),
]


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


class HorariuMasterTableView(NotTeacherMixin, TemplateView):
    template_name = 'horariu/horariu/master_table.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        day_order = {code: i for i, (code, _) in enumerate(_MASTER_DAYS)}

        horarios = Horariu.objects.filter(is_active=True).select_related(
            'horas', 'classe', 'turma', 'departamento',
            'professor_materia__materia',
        )

        hours_map = OrderedDict()
        grouped_rows = OrderedDict()
        code_name_map = {}

        for item in sorted(horarios, key=lambda h: (day_order[h.loron], h.horas.horas_hahu)):
            hours_map.setdefault(item.horas_id, item.horas)
            group_key = (item.classe_id, item.departamento_id)
            group_data = grouped_rows.setdefault(group_key, {
                'classe': item.classe,
                'departamento': item.departamento,
                'turmas': OrderedDict(),
            })
            cell_map = group_data['turmas'].setdefault(item.turma, defaultdict(set))
            code = item.professor_materia.materia.codigo
            code_name_map.setdefault(code, item.professor_materia.materia.materia)
            cell_map[(item.loron, item.horas_id)].add(code)

        hours = list(hours_map.values())
        morning_hours = [h for h in hours if h.horas_hahu.hour < 12]
        afternoon_hours = [h for h in hours if h.horas_hahu.hour >= 12]

        def build_groups(hours_subset):
            groups = []
            for group_data in grouped_rows.values():
                classe = group_data['classe']
                departamento = group_data['departamento']
                dept_code = (departamento.sigla or departamento.departamento or '').strip().lower()
                rows = []
                for turma, cell_map in group_data['turmas'].items():
                    cells = []
                    for day_code, _ in _MASTER_DAYS:
                        for i, hour in enumerate(hours_subset):
                            values = sorted(cell_map.get((day_code, hour.id), []))
                            cells.append({
                                'value': ' / '.join(values),
                                'subject_names': ' / '.join(code_name_map.get(v, v) for v in values),
                                'day_code': day_code,
                                'is_day_start': i == 0,
                            })
                    rows.append({'turma': turma, 'cells': cells})
                groups.append({'group_label': f"{classe.classe} {dept_code}".strip(), 'rows': rows})
            return groups

        materia_rows = []
        materias = list(Materia.objects.order_by('codigo'))
        for i in range(0, len(materias), 6):
            chunk = materias[i:i + 6]
            chunk += [None] * (6 - len(chunk))
            materia_rows.append(chunk)

        ctx.update({
            'days': _MASTER_DAYS,
            'materia_rows': materia_rows,
            'sections': [
                {'label': 'Dader', 'hours': morning_hours, 'groups': build_groups(morning_hours)},
                {'label': 'Tarde', 'hours': afternoon_hours, 'groups': build_groups(afternoon_hours)},
            ],
        })
        return ctx
