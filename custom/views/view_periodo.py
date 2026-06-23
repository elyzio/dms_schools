from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from main.mixins import AdminRequiredMixin, NotTeacherMixin, admin_required
from ..models import Periodo
from ..forms import PeriodoForm


class PeriodoListView(NotTeacherMixin, ListView):
    model = Periodo
    template_name = 'custom/periodo/list.html'
    context_object_name = 'periodos'


class PeriodoCreateView(AdminRequiredMixin, CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'custom/periodo/form.html'
    success_url = reverse_lazy('periodo-list')

    def form_valid(self, form):
        messages.success(self.request, 'Periodo kria ho susesu.')
        return super().form_valid(form)


class PeriodoUpdateView(AdminRequiredMixin, UpdateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'custom/periodo/form.html'
    success_url = reverse_lazy('periodo-list')

    def form_valid(self, form):
        messages.success(self.request, 'Periodo atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def periodo_delete_view(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)
    if request.method == 'POST':
        messages.warning(request, f'Periodo {periodo} hamoos ona.')
        periodo.delete()
    return redirect('periodo-list')
