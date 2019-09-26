from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from StadiumTrackerAPI import settings
from datetime import datetime
from stadium_tracker.venue_details import get_venue_details
import requests


class Venues(models.Model):
    venue_id = models.IntegerField()
    venue_name = models.CharField(max_length=254)
    home_team_id = models.IntegerField()
    division_id = models.IntegerField()
    street_address_1 = models.CharField(max_length=254, null=True, blank=True)
    street_address_2 = models.CharField(max_length=254, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.CharField(max_length=9, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)

    def __str__(self):
        return f'{self.venue_name}'

    def get_division_name(self):
        url = f'http://statsapi.mlb.com/api/v1/divisions/{self.division_id}'
        r = requests.get(url)
        division_name = r.json().get('divisions')[0].get('name')
        return division_name


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

    def get_user_stadium_visited(self):
        visited = GameDetails.objects.filter(venue_id=self.venue_id).filter(user=self.user)
        return visited

    class Meta:
        unique_together = ['user','game_id']

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


