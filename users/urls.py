from django.urls import path
from users.views import UserUpdateView

app_name = 'users'


urlpatterns = [
    path('<int:pk>', UserUpdateView.as_view(template_name='user.html'), name='user'),
]