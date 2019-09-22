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
        widgets = {
            'home_team': forms.HiddenInput(),
            'home_runs': forms.HiddenInput(),
            'home_hits': forms.HiddenInput(),
            'home_errors': forms.HiddenInput(),
            'away_team': forms.HiddenInput(),
            'away_runs': forms.HiddenInput(),
            'away_hits': forms.HiddenInput(),
            'away_errors': forms.HiddenInput(),
            'game_datetime': forms.HiddenInput(),
            'game_headline': forms.HiddenInput(),
            'game_body': forms.HiddenInput(),
            'game_id': forms.HiddenInput(),
            'venue_id': forms.HiddenInput(),
        }