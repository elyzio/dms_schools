from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
    path('ajax/', include('custom.urls')),
    path('estudante/', include('estudante.urls')),
    path('funcionario/', include('funcionario.urls')),
    path('users/', include('users.urls')),
    path('report/', include('report.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
