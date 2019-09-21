import requests


def get_venue_details(venue_id):
    url = f'http://statsapi.mlb.com/api/v1/venues/{venue_id}'
    response = requests.get(url)
    venue_name = None
    if response.status_code == 200:
        venue_name = response.json().get('venues')[0].get('name')
    return venue_name
