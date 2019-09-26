import requests


def get_venue_details(venue_id):
    url = f'http://statsapi.mlb.com/api/v1/venues/{venue_id}'
    response = requests.get(url)
    venue_name = None
    if response.status_code == 200:
        venue_name = response.json().get('venues')[0].get('name')
    return venue_name

def get_venue_list(sportId, division_id):
    d = division_id
    url = 'http://statsapi.mlb.com/api/v1/teams'
    params = {
        'sportId': sportId
    }
    r = requests.get(url, params)
    teams = r.json().get('teams')
    venues = []
    for t in teams:
        team_name = t.get('name')
        venue_name = t.get('venue').get('name')
        venue_id = t.get('venue').get('id')
        league_id = t.get('league').get('id')
        division_id = t.get('division').get('id')
        data = {
            'team_name': team_name,
            'venue_name': venue_name,
            'venue_id': venue_id,
            'league_id': league_id,
            'division_id': division_id,
            'user_visited': None,
            'visit_count': -9,
        }
        if d == division_id:
            venues.append(data)
        venues = sorted(venues, key=lambda venue: (venue['venue_name']))

    return venues

