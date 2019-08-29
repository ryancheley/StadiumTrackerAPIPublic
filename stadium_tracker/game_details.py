from datetime import datetime
import requests


def get_game_details(game_id):
    """
    :param game_id:
    :return: dictionary of game details which includes the Headline, Blurb, and body of the story
    """
    game_url = f'http://statsapi.mlb.com/api/v1/schedule/games?sportId=1&gamePk={game_id}'
    r_game = requests.get(game_url)
    game_date = r_game.json().get('dates')[0].get('games')[0].get('gameDate')

    story_url = f'http://statsapi.mlb.com/api/v1/game/{game_id}/content'
    r_story = requests.get(story_url)
    recap = r_story.json().get('editorial').get('recap').get('mlb')
    headline = None
    blurb = None
    body = None
    if recap is not None:
        headline = recap.get('headline')
        blurb = recap.get('blurb')
        body = recap.get('body')

    boxscore_url = f'http://statsapi.mlb.com/api/v1/game/{game_id}/boxscore'
    r_boxscore = requests.get(boxscore_url)
    boxscore = r_boxscore.json()
    teams = boxscore.get('teams')
    away_team = {
        'hits': teams.get('away').get('teamStats').get('batting').get('hits'),
        'runs': teams.get('away').get('teamStats').get('batting').get('runs'),
        'errors': teams.get('away').get('teamStats').get('fielding').get('errors'),
        'team': teams.get('away').get('team').get('name'),
    }
    home_team = {
        'hits': teams.get('home').get('teamStats').get('batting').get('hits'),
        'runs': teams.get('home').get('teamStats').get('batting').get('runs'),
        'errors': teams.get('home').get('teamStats').get('fielding').get('errors'),
        'team': teams.get('home').get('team').get('name'),
    }

    details = {
        'headline': headline,
        'blurb': blurb,
        'body': body,
        'home': home_team,
        'away': away_team,
        'game_date': datetime.strptime(game_date, '%Y-%m-%dT%H:%M:%SZ'),
        'game_id': game_id,
    }
    return details