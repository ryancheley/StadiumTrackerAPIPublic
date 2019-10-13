from django.test import TestCase, Client, override_settings
from django.urls import reverse
from users.models import CustomUser

from stadium_tracker.views import *


class TestStadiumGamesViewList(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        test_user = CustomUser.objects.create(
            username='testuser',
            password='test',
            favorite_team=119
        )
        test_user.save()

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_StadiumGamesViewList_get_query_set(self):
        response = self.client.get(reverse('stadium_tracker:stadium_game_list', kwargs={'venue_id': 22}))
        self.assertEqual(response.status_code, 200)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_VenueList_get(self):
        response = self.client.get(reverse('stadium_tracker:venue_list'))
        self.assertEqual(response.status_code, 200)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_MyVenues_get_not_logged_in(self):
        response = self.client.get(reverse('stadium_tracker:my_venues'))
        self.assertEqual(response.status_code, 302)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_MyVenues_get_logged_in(self):
        pass
        # response = self.client.get(reverse('stadium_tracker:my_venues'))
        # self.assertEqual(response.status_code, 200)

    def test_GameDetailCreate_get_not_logged_in(self):
        response = self.client.get(reverse('stadium_tracker:gamedetails_create'))
        self.assertEqual(response.status_code, 302)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_GameDetailCreate_get_logged_in(self):
        pass
