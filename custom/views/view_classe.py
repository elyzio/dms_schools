from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from main.mixins import AdminRequiredMixin, NotTeacherMixin, admin_required
from ..models import Classe
from ..forms import ClasseForm


class ClasseListView(NotTeacherMixin, ListView):
    model = Classe
    template_name = 'custom/classe/list.html'
    context_object_name = 'classes'


class ClasseCreateView(AdminRequiredMixin, CreateView):
    model = Classe
    form_class = ClasseForm
    template_name = 'custom/classe/form.html'
    success_url = reverse_lazy('classe-list')

    def form_valid(self, form):
        messages.success(self.request, 'Klase kria ho susesu.')
        return super().form_valid(form)


class ClasseUpdateView(AdminRequiredMixin, UpdateView):
    model = Classe
    form_class = ClasseForm
    template_name = 'custom/classe/form.html'
    success_url = reverse_lazy('classe-list')

    def form_valid(self, form):
        messages.success(self.request, 'Klase atualiza ho susesu.')
        return super().form_valid(form)


@admin_required
def classe_delete_view(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        messages.warning(request, f'Klase {classe} hamoos ona.')
        classe.delete()
    return redirect('classe-list')
