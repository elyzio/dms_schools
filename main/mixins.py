from functools import wraps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


def _is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()


def _is_teacher(user):
    return user.groups.filter(name='professor').exists()


class AdminRequiredMixin(LoginRequiredMixin):
    """Allow only Admin users (or superusers)."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not _is_admin(request.user):
            messages.error(request, 'Asesu la permiti.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class NotTeacherMixin(LoginRequiredMixin):
    """Block Teacher role; Admin and Director can pass."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if _is_teacher(request.user):
            messages.error(request, 'Asesu la permiti.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


def admin_required(view_func):
    """Decorator version of AdminRequiredMixin for function-based views."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        if not _is_admin(request.user):
            messages.error(request, 'Asesu la permiti.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def not_teacher_required(view_func):
    """Decorator version of NotTeacherMixin for function-based views."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        if _is_teacher(request.user):
            messages.error(request, 'Asesu la permiti.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def teacher_required(view_func):
    """Allow only Teacher (professor group) users."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        if not _is_teacher(request.user):
            messages.error(request, 'Asesu la permiti.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def teacher_or_admin_required(view_func):
    """Allow Teacher (professor group) or Admin users — for pages both roles can reach."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        if not (_is_teacher(request.user) or _is_admin(request.user)):
            messages.error(request, 'Asesu la permiti.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
