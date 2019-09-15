from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from StadiumTrackerAPI import settings
from datetime import datetime
from stadium_tracker.game_details import get_game_details
from stadium_tracker.venue_details import get_venue_details


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

    def game_details(self):
        game_details = []
        details = GamesSeen.objects.all()
        for d in details:
            game_details.append(get_game_details(d))
        return game_details

    def get_venue_count(self):
        """

        :return: a list of dictionaries that includes the Venue Name and the Count of times that Venue has been visited
        """
        game_venue = []
        details = GamesSeen.objects.all().values('venue_id').annotate(total=Count('venue_id')).order_by('-total')
        #game_venue = GamesSeen.objects.all().values('venue_id').annotate(total=Count('venue_id')).order_by('-total')
        for d in details:
            game_venue.append({
                'name': get_venue_details(d.get('venue_id')),
                'total': d.get('total')
            })
        return game_venue