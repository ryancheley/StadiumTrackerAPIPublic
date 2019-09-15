from django.test import TestCase
from stadium_tracker.game_details import get_teams, get_game_details, get_game_schedule_details, get_game_team_data\
    , get_game_date
from datetime import datetime


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

    def test_get_game_details_none_headline(self):
        x = get_game_details(415686)
        headline = x.get('headline')
        blurb = x.get('blurb')
        body = x.get('body')
        self.assertEquals(headline, None)
        self.assertEquals(blurb, None)
        self.assertEquals(body, None)

    def test_get_team_details(self):
        x = get_game_details(415686)
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
        self.assertEqual(home_team, 'San Diego Padres')
        self.assertEqual(away_team, 'Los Angeles Dodgers')
        self.assertEqual(home_score, 1)
        self.assertEqual(home_hits, 6)
        self.assertEqual(home_errors, 1)
        self.assertEqual(away_score, 5)
        self.assertEqual(away_hits, 7)
        self.assertEqual(away_errors, 0)
        self.assertEqual(game_date, datetime(2015, 9, 6, 20, 10))
        self.assertEqual(game_id, 415686)


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


class GetGameTeamData(TestCase):

    def test_get_game_team_data_home(self):
        x = get_game_team_data(1, 8060, True)
        team_id = x.get('team_id')
        team_name = x.get('team_name')
        team_score = x .get('team_score')
        self.assertEqual(team_id, 137)
        self.assertEqual(team_name, 'San Francisco Giants')
        self.assertEqual(team_score, 2)

    def test_get_game_team_data_away(self):
        x = get_game_team_data(1, 8060, False)
        team_id = x.get('team_id')
        team_name = x.get('team_name')
        team_score = x .get('team_score')
        self.assertEqual(team_id, 115)
        self.assertEqual(team_name, 'Colorado Rockies')
        self.assertEqual(team_score, 1)


class GetGameDate(TestCase):

    def test_get_game_date(self):
        x = get_game_date(1, 8060)
        self.assertEqual(x, '2001-07-19')