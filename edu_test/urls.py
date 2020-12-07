from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('', include('core.urls')),
    path('sheets/', include('sheets.urls')),
    path('parse/', include('jsonparser.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)