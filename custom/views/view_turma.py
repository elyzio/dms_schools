from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from main.mixins import AdminRequiredMixin, NotTeacherMixin, admin_required
from ..models import Turma
from ..forms import TurmaForm


class TurmaListView(NotTeacherMixin, ListView):
    model = Turma
    template_name = 'custom/turma/list.html'
    context_object_name = 'turmas'


class TurmaCreateView(AdminRequiredMixin, CreateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'custom/turma/form.html'
    success_url = reverse_lazy('turma-list')

    def form_valid(self, form):
        messages.success(self.request, 'Turma kria ho susesu.')
        return super().form_valid(form)


class TurmaUpdateView(AdminRequiredMixin, UpdateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'custom/turma/form.html'
    success_url = reverse_lazy('turma-list')

    def form_valid(self, form):
        messages.success(self.request, 'Turma atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def turma_delete_view(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        messages.warning(request, f'Turma {turma} hamoos ona.')
        turma.delete()
    return redirect('turma-list')
