from django.forms import ModelForm
from django import forms

from .models import GamesSeen


class GameSeenForm(ModelForm):

    class Meta:
        model = GamesSeen
        fields = ['game_id','venue_id',]
        widgets = {'game_id': forms.HiddenInput()}


