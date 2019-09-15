from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from stadium_tracker.game_details import get_game_details, get_teams, get_form_details

from stadium_tracker.models import GamesSeen
from stadium_tracker.forms import GameSeenForm

# Documentation for MLB API http://statsapi-default-elb-prod-876255662.us-east-1.elb.amazonaws.com/docs/


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
        form = GameSeenForm()
        teams = get_teams()
        display_dates = get_form_details(request)

        if display_dates:
            form.fields['game_id'].initial = display_dates[0].get('gamePk')
            form.fields['venue_id'].initial = display_dates[0].get('venue_id')

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


class VenueList(ListView):
    model = GamesSeen

    def get(self, request, *args, **kwargs):
        venues = GamesSeen.get_venue_count(self)

        context = {
            'venues': venues,
        }
        return render(request, 'stadium_tracker/venue_list.html', context)