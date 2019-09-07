import requests


def get_venues():
    url = 'http://statsapi.mlb.com/api/v1/venues'
    response = requests.get(url)
    venues = response.json().get('venues')
    venues = [d for d in venues if d['id'] in range(0,50)]
    venues = sorted(venues, key = lambda venue: (venue['id']))
    venue_display = []
    for i in range(len(venues)):
        venue_display.append({'id': venues[i].get('id'), 'name': venues[i].get('name')})
    return venue_display
