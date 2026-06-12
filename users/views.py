from django.views.generic import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import redirect, render
from django import forms
from main.mixins import AdminRequiredMixin
from funcionario.forms import ProfessorSelfUpdateForm
from .forms import UserProfileForm, ProfilePasswordChangeForm


class UserGroupForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Papel (Role)',
    )


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'users/user/list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.prefetch_related('groups').order_by('username')


class UserGroupUpdateView(AdminRequiredMixin, View):
    template_name = 'users/user/group_form.html'

    def get(self, request, pk):
        target_user = User.objects.get(pk=pk)
        form = UserGroupForm(initial={'groups': target_user.groups.all()})
        return render(request, self.template_name, {'form': form, 'target_user': target_user})

    def post(self, request, pk):
        target_user = User.objects.get(pk=pk)
        form = UserGroupForm(request.POST)
        if form.is_valid():
            target_user.groups.set(form.cleaned_data['groups'])
            messages.success(request, f'Papel ba {target_user.username} atualiza ho susesu.')
            return redirect('user-list')
        return render(request, self.template_name, {'form': form, 'target_user': target_user})


# =============================================================================
# PROFILE VIEWS
# =============================================================================

class UserProfileView(LoginRequiredMixin, View):
    template_name = 'users/profiles/profile.html'

    def get(self, request):
        professor_user = None
        try:
            professor_user = request.user.professoruser
        except Exception:
            pass
        return render(request, self.template_name, {
            'professor_user': professor_user,
        })


class UserProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'users/profiles/form.html'

    def _is_teacher(self, request):
        return request.user.groups.filter(name='professor').exists()

    def _get_professor(self, request):
        try:
            return request.user.professoruser.professor
        except Exception:
            return None

    def get(self, request):
        if self._is_teacher(request):
            professor = self._get_professor(request)
            if professor:
                form = ProfessorSelfUpdateForm(instance=professor)
                return render(request, self.template_name, {'form': form, 'is_professor': True})
        form = UserProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if self._is_teacher(request):
            professor = self._get_professor(request)
            if professor:
                form = ProfessorSelfUpdateForm(request.POST, request.FILES, instance=professor)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Perfil atualiza ho susesu.')
                    return redirect('user-profile')
                return render(request, self.template_name, {'form': form, 'is_professor': True})
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualiza ho susesu.')
            return redirect('user-profile')
        return render(request, self.template_name, {'form': form})


class UserProfilePasswordView(LoginRequiredMixin, View):
    template_name = 'users/profiles/password_form.html'

    def get(self, request):
        form = ProfilePasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfilePasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password1'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password muda ho susesu.')
            return redirect('user-profile')
        return render(request, self.template_name, {'form': form})
