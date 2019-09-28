from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import CustomUser
from users.forms import CustomUserChangeForm


# Create your views here.

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['email', 'username', 'twitter_user', 'instagram_user']
    # form_class = CustomUserChangeForm
    template_name = 'user.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = self.form_class
    #     return context

    # def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs)
    #         user = self.request.user
    #         context = {
    #             'pages': {'title': user},
    #             'user': user,
    #             'fields': ''
    #         }
    #         return context
