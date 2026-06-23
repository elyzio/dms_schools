from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from main.mixins import AdminRequiredMixin, NotTeacherMixin, admin_required
from ..models import Materia
from ..forms import MateriaForm


class MateriaListView(NotTeacherMixin, ListView):
    model = Materia
    template_name = 'custom/materia/list.html'
    context_object_name = 'materias'

    def get_queryset(self):
        return Materia.objects.select_related('departamentu').order_by('codigo')


class MateriaCreateView(AdminRequiredMixin, CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'custom/materia/form.html'
    success_url = reverse_lazy('materia-list')

    def form_valid(self, form):
        messages.success(self.request, 'Materia kria ho susesu.')
        return super().form_valid(form)


class MateriaUpdateView(AdminRequiredMixin, UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'custom/materia/form.html'
    success_url = reverse_lazy('materia-list')

    def form_valid(self, form):
        messages.success(self.request, 'Materia atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def materia_delete_view(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        messages.warning(request, f'Materia {materia} hamoos ona.')
        materia.delete()
    return redirect('materia-list')
