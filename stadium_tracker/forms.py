from django.forms import ModelForm
from django import forms

from .models import GamesSeen


class GameSeenForm(ModelForm):
    # game_id = forms.IntegerField(label='Game ID')
    # venue_id = forms.IntegerField(label='Venue ID')

    class Meta:
        model = GamesSeen
        fields = ['game_id',]
        widgets = {'game_id': forms.HiddenInput()}


