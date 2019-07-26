from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('stadium_tracker.urls')),
    path('backend/', admin.site.urls),
    path(r'accounts/', include('django_registration.backends.activation.urls')),
    path(r'accounts/', include('django.contrib.auth.urls')),
    path(r'api/', include('api.urls')),

]
