from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from main.mixins import AdminRequiredMixin, NotTeacherMixin, admin_required
from ..models import Ano
from ..forms import AnoForm


class AnoListView(NotTeacherMixin, ListView):
    model = Ano
    template_name = 'custom/ano/list.html'
    context_object_name = 'anos'


class AnoCreateView(AdminRequiredMixin, CreateView):
    model = Ano
    form_class = AnoForm
    template_name = 'custom/ano/form.html'
    success_url = reverse_lazy('ano-list')

    def form_valid(self, form):
        messages.success(self.request, 'Ano kria ho susesu.')
        return super().form_valid(form)


class AnoUpdateView(AdminRequiredMixin, UpdateView):
    model = Ano
    form_class = AnoForm
    template_name = 'custom/ano/form.html'
    success_url = reverse_lazy('ano-list')

    def form_valid(self, form):
        messages.success(self.request, 'Ano atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def ano_delete_view(request, pk):
    ano = get_object_or_404(Ano, pk=pk)
    if request.method == 'POST':
        messages.warning(request, f'Ano {ano} hamoos ona.')
        ano.delete()
    return redirect('ano-list')
