from django.test import RequestFactory, TestCase
from stadium_tracker.game_details import *
from stadium_tracker.views import GameDetailCreate
from datetime import datetime


class GetTeamsTestCase(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_count_of_teams(self):
        x = get_teams()
        self.assertEqual(len(x), 30)

    def test_name_of_first_team(self):
        x = get_teams()
        self.assertEqual(x[0].get('name'), 'Arizona Diamondbacks')

    def test_id_of_first_team(self):
        x = get_teams()
        self.assertEqual(x[0].get('id'), 109)

    def test_get_form_details(self):
        pass

    def test_get_game_date(self):
        x = get_game_date(8060)
        self.assertEqual(x, '2001-07-19')

    def test_get_game_story_available(self):
        x = get_game_story(565295).status_code
        self.assertEqual(x, 200)

    def test_get_game_story_unavailable(self):
        y = get_game_story(0).status_code
        self.assertNotEquals(y, 200)

    def test_get_game_date(self):
        x = get_game_date(565295)
        self.assertEqual(x, '2019-09-20')

    def test_get_game_recap_available(self):
        h = get_game_recap(565295, 'headline')
        self.assertEqual(h, 'deGrom throws gem to keep Wild hopes alive')

    def test_get_game_recap_unavailable(self):
        h = get_game_recap(0, 'headline')
        self.assertEqual(h, None)

    def test_get_game_recap_no_element(self):
        unk = get_game_recap(565295, 'a')
        self.assertEqual(unk, None)

    def test_get_score_home_available(self):
        home_score = get_score(1, 565295, 'home')
        self.assertEqual(home_score, 1)

    def test_get_score_away_available(self):
        away_score = get_score(1, 565295, 'away')
        self.assertEqual(away_score, 8)

    def test_get_score_home_unavailable(self):
        home_score = get_score(1, 0, 'home')
        self.assertEqual(home_score, None)

    def test_get_score_away_unavailable(self):
        away_score = get_score(1, 0, 'away')
        self.assertEqual(away_score, None)

    def test_get_form_details_available(self):
        """
            Needs to be written
        :return:
        """
        pass


    def test_get_form_details_unavailable(self):
        """
            Needs to be written
        :return:
        """
        pass
