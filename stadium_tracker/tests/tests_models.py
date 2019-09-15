from django.test import TestCase
from stadium_tracker.models import GamesSeen
from users.models import CustomUser


class GamesSeenModelTest(TestCase):

    def test_string_representation(self):
        game = GamesSeen(game_id=8060, user_id=1)
        self.assertEqual(game.game_id, 8060)
        self.assertEqual(str(game), '8060')
        self.assertNotEquals(str(game), 8060)

    def create_gameseen(self):
        CustomUser.objects.create(
            password='abc123',
            is_superuser=False,
            username='test',
            first_name='test',
            last_name='test',
            email='test@test.com',
            is_active=True,
        )

        x = GamesSeen.objects.create(
            game_id=8060,
            user_id=1,
            venue_id=2395,
        )
        return x

    def test_gameseen_creation(self):
        g = self.create_gameseen()
        self.assertTrue(isinstance(g, GamesSeen))
        self.assertEqual(g.game_id, 8060)
        self.assertEqual(g.user_id, 1)
