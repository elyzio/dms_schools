from django.urls import path
from . import views

urlpatterns = [
    path('subdistritos/', views.ajax_load_subdistritos, name='ajax-load-subdistritos'),
    path('sucos/', views.ajax_load_sucos, name='ajax-load-sucos'),
    path('aldeias/', views.ajax_load_aldeias, name='ajax-load-aldeias'),
]
