from django.contrib import admin
from django.conf import settings
from django.urls import path, include
#from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', include('core.urls')),
    path('sheets/', include('sheets.urls')),
    path('parse/', include('jsonparser.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
]
