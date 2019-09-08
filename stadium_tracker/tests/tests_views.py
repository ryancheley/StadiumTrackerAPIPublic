from django.test import TestCase, override_settings
from django.urls import reverse
from datetime import datetime

from stadium_tracker.models import GamesSeen
from users.models import CustomUser


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class GamesSeenListViewTestCase(TestCase):
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
            GamesSeen.objects.create(
                game_id=game_id,
                create_date=datetime.now,
                modify_date=datetime.now,
                delete_ind=False,
                user_id=1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/stadium/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('stadium_tracker:gamesseen_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('stadium_tracker:gamesseen_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stadium_tracker/gamesseen_list.html')


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
            GamesSeen.objects.create(
                game_id=game_id,
                create_date=datetime.now,
                modify_date=datetime.now,
                delete_ind=False,
                user_id=1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/stadium/games/1')
        self.assertEqual(response.status_code, 200)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class GamesSeenCreateTestCase(TestCase):
    pass


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class GamesSeenCreateTestCase(TestCase):
    pass
