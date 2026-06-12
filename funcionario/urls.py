from django.urls import path
from .views import (
    ProfessorListView, ProfessorDetailView, ProfessorMyProfileView,
    ProfessorCreateView, ProfessorUpdateView, ProfessorSelfUpdateView,
    professor_delete_view, ProfessorUserCreateView,
    ProfessorUserPasswordChangeView,
    ProfessorMateriaListView, ProfessorMateriaCreateView,
    ProfessorMateriaUpdateView, professor_materia_delete_view,
    ProfessorClasseListView, ProfessorClasseCreateView,
    ProfessorClasseUpdateView, professor_klasse_delete_view,
)

urlpatterns = [
    path('', ProfessorListView.as_view(), name='professor-list'),
    path('meu-perfil/', ProfessorMyProfileView.as_view(), name='professor-my-profile'),
    path('meu-perfil/editar/', ProfessorSelfUpdateView.as_view(), name='professor-self-update'),
    path('criar/', ProfessorCreateView.as_view(), name='professor-create'),

    path('materia/', ProfessorMateriaListView.as_view(), name='professor-materia-list'),
    path('materia/criar/', ProfessorMateriaCreateView.as_view(), name='professor-materia-create'),
    path('materia/<int:pk>/editar/', ProfessorMateriaUpdateView.as_view(), name='professor-materia-update'),
    path('materia/<int:pk>/eliminar/', professor_materia_delete_view, name='professor-materia-delete'),

    path('klasse/', ProfessorClasseListView.as_view(), name='professor-klasse-list'),
    path('klasse/criar/', ProfessorClasseCreateView.as_view(), name='professor-klasse-create'),
    path('klasse/<int:pk>/editar/', ProfessorClasseUpdateView.as_view(), name='professor-klasse-update'),
    path('klasse/<int:pk>/eliminar/', professor_klasse_delete_view, name='professor-klasse-delete'),

    path('<int:pk>/', ProfessorDetailView.as_view(), name='professor-detail'),
    path('<int:pk>/editar/', ProfessorUpdateView.as_view(), name='professor-update'),
    path('<int:pk>/eliminar/', professor_delete_view, name='professor-delete'),
    path('<int:pk>/user/', ProfessorUserCreateView.as_view(), name='professor-user'),
    path('<int:pk>/user/password/', ProfessorUserPasswordChangeView.as_view(), name='professor-user-password'),
]
