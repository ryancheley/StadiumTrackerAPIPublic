from django.db import models
from django.contrib.auth.models import User
from StadiumTrackerAPI import settings
from datetime import datetime
from .game_details import get_game_details


class GamesSeen(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game_id = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now_add=True)
    delete_ind = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.game_id}'

    def save(self, *args, **kwargs):
        self.modify_date = datetime.now()
        super(GamesSeen, self).save(*args, **kwargs)

    def game_details(self):
        game_details = []
        details = GamesSeen.objects.all()
        for d in details:
            game_details.append(get_game_details(d))
        return game_details

    class Meta:
        ordering = ['-modify_date']
