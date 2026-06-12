from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from main.mixins import AdminRequiredMixin, NotTeacherMixin, admin_required
from .models import Professor, ProfessorUser, ProfessorClasse, ProfessorMateria
from .forms import (
    ProfessorForm, ProfessorSelfUpdateForm, ProfessorUserForm,
    ProfessorUserPasswordChangeForm, ProfessorMateriaForm, ProfessorClasseForm,
)


class ProfessorListView(NotTeacherMixin, ListView):
    model = Professor
    template_name = 'funcionario/professor/list.html'
    context_object_name = 'professores'

    def get_queryset(self):
        qs = Professor.objects.filter(is_delete=False)
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(nome__icontains=q) | Q(numero_funcionario__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class ProfessorDetailView(LoginRequiredMixin, DetailView):
    model = Professor
    template_name = 'funcionario/professor/detail.html'
    context_object_name = 'professor'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='professor').exists():
            try:
                own_pk = request.user.professoruser.professor.pk
            except Exception:
                messages.error(request, 'Asesu la permiti.')
                return redirect('dashboard')
            if int(kwargs.get('pk', 0)) != own_pk:
                messages.error(request, 'Asesu la permiti.')
                return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classes'] = self.object.professorclasse_set.select_related(
            'ano', 'classe', 'turma'
        ).order_by('-ano__ano')
        ctx['materias'] = self.object.professormateria_set.select_related(
            'materia', 'classe'
        ).order_by('classe__classe')
        try:
            ctx['professor_user'] = self.object.professoruser
        except ProfessorUser.DoesNotExist:
            ctx['professor_user'] = None
        return ctx


class ProfessorMyProfileView(LoginRequiredMixin, View):
    """Redirect the logged-in professor to their own profile detail page."""

    def get(self, request):
        try:
            professor_user = ProfessorUser.objects.get(user=request.user)
            return redirect('professor-detail', pk=professor_user.professor.pk)
        except ProfessorUser.DoesNotExist:
            messages.error(request, 'Perfil professor la hetan.')
            return redirect('dashboard')


class ProfessorCreateView(AdminRequiredMixin, CreateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'funcionario/professor/form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        professor = self.object
        emis = (professor.emis_prof or '').strip().lower()

        if not emis:
            messages.warning(
                self.request,
                'EMIS Prof mamuk — utilizador la kria automaticamente. Bele kria manualmente depois.'
            )
            return response

        if User.objects.filter(username=emis).exists():
            messages.warning(
                self.request,
                f'Username "{emis}" uza tiha ona — utilizador la kria automaticamente.'
            )
            return response

        user = User.objects.create_user(username=emis, password='Password_1234')
        group, _ = Group.objects.get_or_create(name='professor')
        user.groups.add(group)
        ProfessorUser.objects.create(professor=professor, user=user)
        messages.info(
            self.request,
            f'Utilizador "{emis}" kria automaticamente ho password default: Password_1234'
        )
        return response

    def get_success_url(self):
        messages.success(self.request, f'Funcionario {self.object.nome} rejistadu ho susesu.')
        return reverse('professor-detail', kwargs={'pk': self.object.pk})


class ProfessorUpdateView(AdminRequiredMixin, UpdateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'funcionario/professor/form.html'

    def get_success_url(self):
        messages.success(self.request, f'Dados {self.object.nome} atualiza ho susesu.')
        return reverse('professor-detail', kwargs={'pk': self.object.pk})


@admin_required
def professor_delete_view(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        professor.is_delete = True
        professor.is_active = False
        professor.save()
        messages.warning(request, f'Funcionario {professor.nome} hamoos ona husi sistema.')
        return redirect('professor-list')
    return redirect('professor-detail', pk=pk)


class ProfessorSelfUpdateView(LoginRequiredMixin, UpdateView):
    """Professors update their own non-principal data. No PK in URL."""
    model = Professor
    form_class = ProfessorSelfUpdateForm
    template_name = 'funcionario/professor/self_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='professor').exists():
            messages.error(request, 'Asesu la permiti.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return self.request.user.professoruser.professor
        except Exception:
            messages.error(self.request, 'Perfil professor la hetan.')
            return redirect('dashboard')

    def get_success_url(self):
        messages.success(self.request, 'Perfil atualiza ho susesu.')
        return reverse('professor-detail', kwargs={'pk': self.object.pk})


class ProfessorUserCreateView(AdminRequiredMixin, FormView):
    form_class = ProfessorUserForm
    template_name = 'funcionario/professorUser/form.html'

    def get_professor(self):
        return get_object_or_404(Professor, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['professor'] = self.get_professor()
        return ctx

    def form_valid(self, form):
        professor = self.get_professor()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        role = form.cleaned_data['role']

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=professor.nome.split()[0] if professor.nome else '',
        )
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        ProfessorUser.objects.create(professor=professor, user=user)
        messages.success(self.request, f'Utilizador "{username}" kria ho susesu.')
        return redirect('professor-detail', pk=professor.pk)


class ProfessorUserPasswordChangeView(AdminRequiredMixin, FormView):
    form_class = ProfessorUserPasswordChangeForm
    template_name = 'funcionario/professorUser/password_form.html'

    def get_professor_user(self):
        return get_object_or_404(ProfessorUser, professor__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['professor_user'] = self.get_professor_user()
        ctx['professor'] = ctx['professor_user'].professor
        return ctx

    def form_valid(self, form):
        professor_user = self.get_professor_user()
        professor_user.user.set_password(form.cleaned_data['password1'])
        professor_user.user.save()
        messages.success(self.request, f'Password ba utilizador "{professor_user.user.username}" troka ho susesu.')
        return redirect('professor-detail', pk=professor_user.professor.pk)


# =============================================================================
# PROFESSOR MATERIA (subject assignment)
# =============================================================================

class ProfessorMateriaListView(NotTeacherMixin, ListView):
    model = ProfessorMateria
    template_name = 'funcionario/professorMateria/list.html'
    context_object_name = 'atribuisoes'

    def get_queryset(self):
        qs = ProfessorMateria.objects.select_related('professor', 'materia', 'classe').order_by('professor__nome', 'classe__classe')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(professor__nome__icontains=q) |
                Q(materia__materia__icontains=q) |
                Q(classe__classe__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class ProfessorMateriaCreateView(AdminRequiredMixin, CreateView):
    model = ProfessorMateria
    form_class = ProfessorMateriaForm
    template_name = 'funcionario/professorMateria/form.html'
    success_url = reverse_lazy('professor-materia-list')

    def form_valid(self, form):
        messages.success(self.request, 'Atribuisaun materia kria ho susesu.')
        return super().form_valid(form)


class ProfessorMateriaUpdateView(AdminRequiredMixin, UpdateView):
    model = ProfessorMateria
    form_class = ProfessorMateriaForm
    template_name = 'funcionario/professorMateria/form.html'
    success_url = reverse_lazy('professor-materia-list')

    def form_valid(self, form):
        messages.success(self.request, 'Atribuisaun materia atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def professor_materia_delete_view(request, pk):
    atribuisaun = get_object_or_404(ProfessorMateria, pk=pk)
    if request.method == 'POST':
        messages.warning(
            request,
            f'Atribuisaun {atribuisaun.materia.materia} ba {atribuisaun.professor.nome} hamoos ona.'
        )
        atribuisaun.delete()
    return redirect('professor-materia-list')


# =============================================================================
# PROFESSOR KLASSE (class assignment)
# =============================================================================

class ProfessorClasseListView(NotTeacherMixin, ListView):
    model = ProfessorClasse
    template_name = 'funcionario/professorKlasse/list.html'
    context_object_name = 'atribuisoes'

    def get_queryset(self):
        qs = ProfessorClasse.objects.select_related('professor', 'ano', 'departamento', 'classe', 'turma').order_by('-ano__ano', 'professor__nome')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(professor__nome__icontains=q) |
                Q(classe__classe__icontains=q) |
                Q(turma__turma__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class ProfessorClasseCreateView(AdminRequiredMixin, CreateView):
    model = ProfessorClasse
    form_class = ProfessorClasseForm
    template_name = 'funcionario/professorKlasse/form.html'
    success_url = reverse_lazy('professor-klasse-list')

    def form_valid(self, form):
        messages.success(self.request, 'Atribuisaun klase kria ho susesu.')
        return super().form_valid(form)


class ProfessorClasseUpdateView(AdminRequiredMixin, UpdateView):
    model = ProfessorClasse
    form_class = ProfessorClasseForm
    template_name = 'funcionario/professorKlasse/form.html'
    success_url = reverse_lazy('professor-klasse-list')

    def form_valid(self, form):
        messages.success(self.request, 'Atribuisaun klase atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def professor_klasse_delete_view(request, pk):
    atribuisaun = get_object_or_404(ProfessorClasse, pk=pk)
    if request.method == 'POST':
        messages.warning(
            request,
            f'Atribuisaun klase {atribuisaun.classe.classe} ba {atribuisaun.professor.nome} hamoos ona.'
        )
        atribuisaun.delete()
    return redirect('professor-klasse-list')
