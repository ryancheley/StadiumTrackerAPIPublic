import requests


def get_division_details(sportId):
    url = 'http://statsapi.mlb.com/api/v1/divisions'
    params = {
        'sportId': sportId
    }
    r = requests.get(url, params)
    divisions = []
    div_json = r.json().get('divisions')
    for d in div_json:
        default_division = False
        division_id = d.get('id')
        division_name = d.get('nameShort')
        if division_id == 203:
            default_division = True
        data = {
            'division_id': division_id,
            'division_name': division_name,
            'default_division': default_division
        }
        divisions.append(data)
        divisions = sorted(divisions, key=lambda division: (division['division_name']))
    return divisions