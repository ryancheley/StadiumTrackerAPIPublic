from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from stadium_tracker.game_details import *

from stadium_tracker.models import GameDetails
from stadium_tracker.forms import GameDetailsForm


class GamesViewList(ListView):
    model = GameDetails
    context_object_name = 'game_list'
    template_name = 'stadium_tracker/game_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['details'] = GameDetails.objects.all()
        return data


class GameDetailView(DetailView):
    model = GameDetails
    context_object_name = 'details'
    template_name = 'stadium_tracker/gamedetails_view.html'


class VenueList(ListView):
    model = GameDetails
    template_name = 'stadium_tracker/venue_list.html'

    def get(self, request, *args, **kwargs):
        venues = GameDetails.get_venue_count(self)

        context = {
            'venues': venues,
        }
        return render(request, 'stadium_tracker/venue_list.html', context)


class GameDetailCreate(LoginRequiredMixin, CreateView):
    model = GameDetails
    form_class = GameDetailsForm
    template_name = 'stadium_tracker/gamedetails_create.html'
    success_url = reverse_lazy('stadium_tracker:game_list')

    def get_queryset(self):
        """
        This is mostly a place holder for now
        :return:
        """
        pass

    def get(self, request, *args, **kwargs):
        form = GameDetailsForm()
        teams = get_teams()
        display_dates = get_form_details(request)
        if len(request.GET)>0:
            game_details = get_game_details(display_dates[0].get('gamePk'))
            game_id = game_details.get('game_id')
            headline = get_game_recap(game_id, 'headline')
            body = get_game_recap(game_id, 'body')
            home_details = get_boxscore(game_id, 'home')
            away_details = get_boxscore(game_id, 'away')
            game_date = get_game_date(1, game_id)

            if game_details:
                form.fields['game_headline'].initial = headline
                form.fields['game_body'].initial = body
                form.fields['home_team'].initial = home_details.get('team')
                form.fields['home_hits'].initial = home_details.get('hits')
                form.fields['home_runs'].initial = home_details.get('runs')
                form.fields['home_errors'].initial = home_details.get('errors')
                form.fields['away_team'].initial = away_details.get('team')
                form.fields['away_hits'].initial = away_details.get('hits')
                form.fields['away_runs'].initial = away_details.get('runs')
                form.fields['away_errors'].initial = away_details.get('errors')
                form.fields['game_datetime'].initial = game_date
                form.fields['game_id'].initial = game_id
                form.fields['venue_id'].initial = game_details.get('game_venue').get('id')

        context = {
            'form': form,
            'teams': teams,
            'games': display_dates,
            'test': request.GET
        }
        return render(request, 'stadium_tracker/gamedetails_form.html', context)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GameDetailDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GameDetails
    context_object_name = 'game_details'
    success_url = reverse_lazy('stadium_tracker:game_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user