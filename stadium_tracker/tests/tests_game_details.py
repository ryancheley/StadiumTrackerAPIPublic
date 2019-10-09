from django.test import TestCase
from stadium_tracker.game_details import *


class GameDetails(TestCase):

    def test_get_game_recap_headline_is_None(self):
        x = get_game_recap(8060, 'headline')
        self.assertIsNone(x)

    def test_get_game_recap_body_is_None(self):
        x = get_game_recap(8060, 'body')
        self.assertIsNone(x)

    def test_get_game_recap_headline_is_not_None(self):
        x = get_game_recap(566063, 'headline')
        self.assertIsNotNone(x)
        self.assertEqual(x, 'Dodgers rally in NY, clinch NLDS advantage')

    def test_get_game_recap_body_is_not_None(self):
        x = get_game_recap(566063, 'body')
        self.assertIsNotNone(x)
        self.assertEqual(len(x), 3881)

    def test_get_default_game(self):
        x = get_default_game(1)
        self.assertIsNotNone(x.get('game_date'))
        self.assertIsNotNone(x.get('home_team'))
        self.assertIsNotNone(x.get('away_team'))