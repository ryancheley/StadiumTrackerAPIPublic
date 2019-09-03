from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from stadium_tracker.game_details import get_game_details, get_teams

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
        # TODO: Clean up this method as it seems really long
        # TODO: Fix issue with the last game returned being the game ID for all games displayed, look at FormSets
        form = GameSeenForm
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
                        form = GameSeenForm(initial={'game_id': gamePk})

        context = {
            'form': form,
            'teams': teams,
            'games': display_dates,
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