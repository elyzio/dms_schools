from django import template

register = template.Library()


@register.filter
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()


@register.filter
def is_director(user):
    return user.groups.filter(name='diretor').exists()


@register.filter
def is_teacher(user):
    return user.groups.filter(name='professor').exists()
