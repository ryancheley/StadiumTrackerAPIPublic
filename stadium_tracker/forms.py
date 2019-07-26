from django.forms import ModelForm

from .models import GamesSeen


class GameSeenForm(ModelForm):
    class Meta:
        model = GamesSeen
        fields = ['game_id', ]