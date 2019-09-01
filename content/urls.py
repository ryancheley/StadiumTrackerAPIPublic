from django.urls import path
from content.views import ContentTemplateView

app_name = 'stadium_tracker'


urlpatterns = [
    path('', ContentTemplateView.as_view(template_name='page.html'), name='home'),
    path('Pages/<name>', ContentTemplateView.as_view(template_name='page.html'), name='<name>'),
]