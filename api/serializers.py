from rest_framework import serializers

from stadium_tracker.models import GamesSeen


class GamesSeenSerializer(serializers.ModelSerializer):

    class Meta:
        model = GamesSeen
        fields = ('user', 'game_id',)