from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import GamesSeen
from .forms import GameSeenForm


class GamesSeenListView(ListView):
    model = GamesSeen
    context_object_name = 'gamesseen_list'
    test = 'hello'


class GamesSeenDetailView(DetailView):
    model = GamesSeen
    template_name = 'stadium_tracker/gamesseen_detail.html'
    context_object_name = 'game'


class GamesSeenCreate(LoginRequiredMixin, CreateView):
    model = GamesSeen
    form_class = GameSeenForm
    success_url = reverse_lazy('stadium_tracker:gamesseen_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GamesSeenUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GamesSeen
    form_class = GameSeenForm
    success_url = reverse_lazy('stadium_tracker:gamesseen_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class GamesSeenDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GamesSeen
    success_url = reverse_lazy('stadium_tracker:gamesseen_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
