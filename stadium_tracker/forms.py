from django.forms import ModelForm
from django import forms

from .models import GamesSeen, GameDetails


class GameSeenForm(ModelForm):

    class Meta:
        model = GamesSeen
        fields = ['game_id','venue_id',]
        widgets = {
            'game_id': forms.HiddenInput(),
            'venue_id': forms.HiddenInput(),
        }


class GameDetailsForm(ModelForm):

    class Meta:
        model = GameDetails
        fields = [
            'home_team',
            'home_runs',
            'home_hits',
            'home_errors',
            'away_team',
            'away_runs',
            'away_hits',
            'away_errors',
            'game_datetime',
            'game_headline',
            'game_body',
            'game_id',
            'venue_id'
        ]