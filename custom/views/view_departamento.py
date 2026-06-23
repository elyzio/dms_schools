from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from main.mixins import AdminRequiredMixin, NotTeacherMixin, admin_required
from ..models import Departamento
from ..forms import DepartamentoForm


class DepartamentoListView(NotTeacherMixin, ListView):
    model = Departamento
    template_name = 'custom/departamento/list.html'
    context_object_name = 'departamentos'


class DepartamentoCreateView(AdminRequiredMixin, CreateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'custom/departamento/form.html'
    success_url = reverse_lazy('departamento-list')

    def form_valid(self, form):
        messages.success(self.request, 'Departamentu kria ho susesu.')
        return super().form_valid(form)


class DepartamentoUpdateView(AdminRequiredMixin, UpdateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'custom/departamento/form.html'
    success_url = reverse_lazy('departamento-list')

    def form_valid(self, form):
        messages.success(self.request, 'Departamentu atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def departamento_delete_view(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        messages.warning(request, f'Departamentu {departamento} hamoos ona.')
        departamento.delete()
    return redirect('departamento-list')
