from django.test import TestCase
from stadium_tracker.venue_details import get_venues


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
