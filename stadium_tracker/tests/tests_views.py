from django.test import TestCase, override_settings
from django.urls import reverse
from datetime import datetime

from stadium_tracker.models import GameDetails
from users.models import CustomUser


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class GamesSeenListViewTestCase(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/stadium/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('stadium_tracker:game_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('stadium_tracker:game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stadium_tracker/game_list.html')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class GamesSeenDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(
            password='abc123',
            is_superuser=False,
            username='test',
            first_name='test',
            last_name='test',
            email='test@test.com',
            is_active=True,
        )

        games_to_test = [
            448469,
            491328,
            565749,
            566611,
            8060,
            566610,
        ]

        for game_id in games_to_test:
            GameDetails.objects.create(
                game_id=game_id,
                home_team='Dodgers',
                home_runs=5,
                home_hits=5,
                home_errors=0,
                away_team='Giants',
                away_runs=0,
                away_hits=0,
                away_errors=0,
                game_datetime=datetime(2019, 9,27),
                game_body='Lots of Text',
                game_headline='Giants Suck!',
                venue_id=5,
                user_id=1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/stadium/games/1')
        self.assertEqual(response.status_code, 200)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class GamesSeenCreateTestCase(TestCase):
    pass


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class GamesSeenDeleteTestCase(TestCase):
    pass


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class VenueListTestCase(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/stadium/venues')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('stadium_tracker:venue_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('stadium_tracker:venue_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stadium_tracker/venue_list.html')
