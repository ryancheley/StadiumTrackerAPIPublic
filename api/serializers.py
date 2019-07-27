from rest_framework import serializers

from stadium_tracker.models import GamesSeen
from users.models import CustomUser


class GamesSeenSerializer(serializers.ModelSerializer):

    class Meta:
        model = GamesSeen
        fields = ('user', 'game_id',)


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')