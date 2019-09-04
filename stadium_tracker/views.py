from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from stadium_tracker.game_details import get_game_details, get_teams, get_form_details

import requests

from stadium_tracker.models import GamesSeen
from stadium_tracker.forms import GameSeenForm

# Documentation for MLB APIhttp://statsapi-default-elb-prod-876255662.us-east-1.elb.amazonaws.com/docs/


class GamesSeenListView(ListView):
    model = GamesSeen
    context_object_name = 'gamesseen_list'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['details'] = zip(GamesSeen.game_details(GamesSeen.game_id), GamesSeen.objects.all())
        return data


class GamesSeenDetailView(DetailView):
    model = GamesSeen
    context_object_name = 'gamesseen_detail'

    def get(self, request, *args, **kwargs):
        gamePk = GamesSeen.objects.get(pk=self.kwargs['pk'])
        game_details = get_game_details(gamePk)
        context = {
            'game_details': game_details,
        }
        return render(request, 'stadium_tracker/gamesseen_detail.html', context)


class GamesSeenCreate(LoginRequiredMixin, CreateView):
    model = GamesSeen
    form_class = GameSeenForm
    success_url = reverse_lazy('stadium_tracker:gamesseen_list')

    def get(self, request, *args, **kwargs):
        # TODO: Fix issue with the last game returned being the game ID for all games displayed, look at FormSets
        form = GameSeenForm
        teams = get_teams()
        display_dates = get_form_details(request)

        context = {
            'form': form,
            'teams': teams,
            'games': display_dates,
        }
        return render(request, 'stadium_tracker/gamesseen_form.html', context)

    def post(self, request, *args, **kwargs):
        form = GameSeenForm
        teams = get_teams()
        game = GamesSeen()
        game.game_id = int(request.POST.get('name'))
        game.user_id = request.user.id
        game.save()

        context = {
            'form': form,
            'teams': teams,
            'games': None,
        }

        return render(request, 'stadium_tracker/gamesseen_form.html', context)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GamesSeenDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GamesSeen
    success_url = reverse_lazy('stadium_tracker:gamesseen_list')

    def get(self, request, *args, **kwargs):
        gamePk = GamesSeen.objects.get(pk=self.kwargs['pk'])
        game_details = get_game_details(gamePk)
        context = {
            'game_details': game_details,
        }
        return render(request, 'stadium_tracker/gamesseen_confirm_delete.html', context)

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user