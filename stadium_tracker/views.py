from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render

import requests

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


def search_games(request):
    sportId = 1
    team1 = request.GET.get('team1')
    team2 = request.GET.get('team2')
    teamId = f'{team1},{team2}'
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    params = {
        'sportId': sportId,
        'teamId': teamId,
        'startDate': start_date,
        'endDate': end_date
    }

    url = 'http://statsapi.mlb.com/api/v1/schedule/games'
    r = requests.get(url, params)
    games_dates = r.json().get('dates')
    display_dates = []
    teams = get_teams()
    if games_dates is not None:
        for i in range(len(games_dates)):
            date = games_dates[i].get('date')
            for j in range(len(games_dates[i].get('games'))):
                away = games_dates[i].get('games')[j].get('teams').get('away').get('team').get('name')
                away_id = games_dates[i].get('games')[j].get('teams').get('away').get('team').get('id')
                home = games_dates[i].get('games')[j].get('teams').get('home').get('team').get('name')
                home_id = games_dates[i].get('games')[j].get('teams').get('home').get('team').get('id')
                away_score = games_dates[i].get('games')[j].get('teams').get('away').get('score')
                home_score = games_dates[i].get('games')[j].get('teams').get('home').get('score')
                text = f'{date}: {away} vs {home}. Final Score: {away_score} - {home_score}'
                gamePk = games_dates[i].get('games')[j].get('gamePk')
                data = {
                    'text': text,
                    'gamePk': gamePk
                }
                if (str(home_id) == team1 and str(away_id) == team2) or (str(home_id) == team2 and str(away_id) == team1):
                    display_dates.append(data)

    return render(request, 'stadium_tracker/game_search.html', {
        'games': display_dates,
        'teams': teams,
    })


def get_teams():
    url = 'http://statsapi.mlb.com/api/v1/teams?sportId=1'
    r = requests.get(url)
    teams = r.json().get('teams')
    team_display = []
    for i in range(len(teams)):
        team_display.append({'id': teams[i].get('id'), 'name': teams[i].get('name')})
    return team_display
