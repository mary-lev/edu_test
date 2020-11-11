from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('core.urls')),
    path('sheets/', include('sheets.urls')),
    path('parse/', include('jsonparser.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
