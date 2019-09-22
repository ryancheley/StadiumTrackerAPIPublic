from django.test import TestCase
from stadium_tracker.models import GamesSeen, GameDetails
from users.models import CustomUser
from datetime import datetime


class GameDetailsTest(TestCase):

    def create_gamedetails(self, home_team, away_team, game_headline):
        CustomUser.objects.create(
            password='abc123',
            is_superuser=False,
            username='test',
            first_name='test',
            last_name='test',
            email='test@test.com',
            is_active=True,
        )

        x = GameDetails.objects.create(
            game_id=8060,
            home_team=home_team,
            home_runs=5,
            home_hits=5,
            home_errors=0,
            away_team=away_team,
            away_runs=0,
            away_hits=0,
            away_errors=0,
            game_datetime=datetime(2019, 9, 27),
            game_body='Lots of Text',
            game_headline=game_headline,
            venue_id=5,
            user_id=1,
        )
        return x

    def test_gamedetail_creation(self):
        g = self.create_gamedetails('Dodgers', 'Giants', 'Giants Suck!')
        self.assertTrue(isinstance(g, GameDetails))
        self.assertEqual(g.game_id, 8060)
        self.assertEqual(g.user_id, 1)
        self.assertEqual(g.home_team, 'Dodgers')
        self.assertEqual(g.home_runs, 5)
        self.assertEqual(g.home_hits, 5)
        self.assertEqual(g.home_errors, 0)
        self.assertEqual(g.away_team, 'Giants')
        self.assertEqual(g.away_runs, 0)
        self.assertEqual(g.away_hits, 0)
        self.assertEqual(g.away_errors, 0)
        self.assertEqual(g.game_datetime, datetime(2019, 9, 27))
        self.assertEqual(g.game_body, 'Lots of Text')
        self.assertEqual(g.game_headline, 'Giants Suck!')
        self.assertEqual(g.venue_id, 5)
        self.assertEqual(g.user_id, 1)