from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from StadiumTrackerAPI import settings
from datetime import datetime
from stadium_tracker.venue_details import get_venue_details


class GameDetails(models.Model):
    home_team = models.CharField(max_length=100)
    home_runs = models.IntegerField()
    home_hits = models.IntegerField()
    home_errors = models.IntegerField()
    away_team = models.CharField(max_length=100)
    away_runs = models.IntegerField()
    away_hits = models.IntegerField()
    away_errors = models.IntegerField()
    game_datetime = models.DateTimeField()
    game_headline = models.CharField(max_length=254)
    game_body = models.TextField()
    game_id = models.IntegerField()
    venue_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.modify_date = datetime.now()
        super(GameDetails, self).save(*args, **kwargs)

    def get_venue_count(self):
        game_venue = []
        details = GameDetails.objects.all().values('venue_id').annotate(total=Count('venue_id')).order_by('-total')
        for d in details:
            game_venue.append({
                'venue_id': d.get('venue_id'),
                'name': get_venue_details(d.get('venue_id')),
                'total': d.get('total')
            })
        return game_venue

class GamesSeen(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game_id = models.IntegerField()
    venue_id = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now_add=True)
    delete_ind = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.game_id}'

    def save(self, *args, **kwargs):
        self.modify_date = datetime.now()
        super(GamesSeen, self).save(*args, **kwargs)