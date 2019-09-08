from django.test import TestCase
from stadium_tracker.venue_details import get_venues
from stadium_tracker.game_details import get_teams, get_game_details, get_game_schedule_details
from datetime import datetime


class VenueTestCase(TestCase):

    def test_count_of_venues(self):
        x = get_venues()
        self.assertEqual(len(x), 32)

    def test_name_of_first_venue(self):
        x = get_venues()
        self.assertEqual(x[0].get('name'), '3Com Park at Candlestick Point')

    def test_id_of_first_venue(self):
        x = get_venues()
        self.assertEqual(x[0].get('id'), 29)


class GetTeamsTestCase(TestCase):

    def test_count_of_teams(self):
        x = get_teams()
        self.assertEqual(len(x), 30)

    def test_name_of_first_team(self):
        x = get_teams()
        self.assertEqual(x[0].get('name'), 'Arizona Diamondbacks')

    def test_id_of_first_team(self):
        x = get_teams()
        self.assertEqual(x[0].get('id'), 109)


class GameDetailsTestCase(TestCase):

    def test_get_game_details_none(self):
        x = get_game_details(8060)
        headline = x.get('headline')
        blurb = x.get('blurb')
        body = x.get('body')
        self.assertEqual(headline, None)
        self.assertEqual(blurb, None)
        self.assertEqual(body, None)

    def test_get_game_details_not_none_headline(self):
        x = get_game_details(566610)
        headline = x.get('headline')
        blurb = x.get('blurb')
        body = x.get('body')
        self.assertNotEquals(headline, None)
        self.assertNotEquals(blurb, None)
        self.assertNotEquals(body, None)

    def test_get_team_details(self):
        x = get_game_details(566610)
        home_team = x.get('home').get('team')
        away_team = x.get('away').get('team')
        home_score = x.get('home').get('runs')
        home_hits = x.get('home').get('hits')
        home_errors = x.get('home').get('errors')
        away_score = x.get('away').get('runs')
        away_hits = x.get('away').get('hits')
        away_errors = x.get('away').get('errors')
        game_date = x.get('game_date')
        game_id = x.get('game_id')
        self.assertEqual(home_team, 'St. Louis Cardinals')
        self.assertEqual(away_team, 'Arizona Diamondbacks')
        self.assertEqual(home_score, 2)
        self.assertEqual(home_hits, 4)
        self.assertEqual(home_errors, 0)
        self.assertEqual(away_score, 4)
        self.assertEqual(away_hits, 6)
        self.assertEqual(away_errors, 1)
        self.assertEqual(game_date, datetime(2019, 7, 13, 0, 15))
        self.assertEqual(game_id, 566610)


class GameScheduleDetailsTestCase(TestCase):

    def test_get_game_schedule_details_text(self):
        x = get_game_schedule_details(1, 8060)
        text = x.get('text')
        self.assertEqual(text, '2001-07-19: Colorado Rockies vs San Francisco Giants. Final Score: 1 - 2')

    def test_get_game_schedule_details_game_id(self):
        x = get_game_schedule_details(1, 8060)
        game_id = x.get('gamePk')
        self.assertEqual(game_id, 8060)

class GetFormDetailsTestCase(TestCase):

    def test_get_form_details(self):
        pass
