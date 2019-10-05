from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import CustomUser
from users.forms import CustomUserChangeForm
from django.urls import reverse

# Create your views here.

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    # fields = ['email', 'username', 'twitter_user', 'instagram_user', 'favorite_team']
    form_class = CustomUserChangeForm
    template_name = 'user.html'

    def get_success_url(self):
        return reverse('users:user', kwargs={
            'pk': self.object.pk,
        })