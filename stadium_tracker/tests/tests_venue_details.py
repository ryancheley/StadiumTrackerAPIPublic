from django.test import TestCase
from stadium_tracker.venue_details import get_venue_details


class VenueTestCase(TestCase):

    def test_return_name_when_valid_id_passed(self):
        v = get_venue_details(1)
        self.assertEqual(v, 'Angel Stadium')

    def test_return_none_when_invalid_id_passed(self):
        v_num = get_venue_details(0)
        v_string = get_venue_details('A')
        self.assertEqual(v_num, None)
        self.assertEqual(v_string, None)

