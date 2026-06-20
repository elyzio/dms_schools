from django.urls import path
from .views import (
    estudante_list_view, estudante_detail_view,
    estudante_create_view, estudante_update_view,
    estudante_delete_view, estudante_matricula_create_view,
    estudante_transfer_create_view,
    estudante_passa_view, estudante_passa_list_view,
    estudante_reinskrisaun_list_view,
    estudante_alumni_candidates_view, estudante_alumni_list_view, estudante_alumni_create_view,
)

urlpatterns = [
    path('', estudante_list_view, name='estudante-list'),
    path('criar/', estudante_create_view, name='estudante-create'),
    path('passa/', estudante_passa_list_view, name='estudante-passa-list'),
    path('reinskrisaun/', estudante_reinskrisaun_list_view, name='estudante-reinskrisaun-list'),
    path('alumni/', estudante_alumni_candidates_view, name='estudante-alumni-candidates'),
    path('alumni/lista/', estudante_alumni_list_view, name='estudante-alumni-list'),
    path('<int:pk>/', estudante_detail_view, name='estudante-detail'),
    path('<int:pk>/editar/', estudante_update_view, name='estudante-update'),
    path('<int:pk>/eliminar/', estudante_delete_view, name='estudante-delete'),
    path('<int:pk>/matricula/', estudante_matricula_create_view, name='estudante-matricula'),
    path('<int:pk>/transferensia/', estudante_transfer_create_view, name='estudante-transfer'),
    path('<int:pk>/passa/', estudante_passa_view, name='estudante-passa'),
    path('<int:pk>/alumni/criar/', estudante_alumni_create_view, name='estudante-alumni-create'),
]
