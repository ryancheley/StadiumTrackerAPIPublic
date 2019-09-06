from datetime import datetime
import requests


def get_game_details(game_id):
    # TODO: Use GameID 8060 as a test for this method as it will return None and break stuff
    # TODO: Get Team Names and Final Score from same API endpoint as get_form_details
    """
    :param game_id:
    :return: dictionary of game details which includes the Headline, Blurb, and body of the story
    """
    game_url = f'http://statsapi.mlb.com/api/v1/schedule/games?sportId=1&gamePk={game_id}'
    r_game = requests.get(game_url)
    game_date = r_game.json().get('dates')[0].get('games')[0].get('gameDate')

    headline = None
    blurb = None
    body = None
    home_team = None
    away_team = None

    story_url = f'http://statsapi.mlb.com/api/v1/game/{game_id}/content'
    r_story = requests.get(story_url)
    if r_story.json().get('editorial') is not None:
        recap = r_story.json().get('editorial').get('recap').get('mlb')
        headline = recap.get('headline')
        blurb = recap.get('blurb')
        body = recap.get('body')

    boxscore_url = f'http://statsapi.mlb.com/api/v1/game/{game_id}/boxscore'
    r_boxscore = requests.get(boxscore_url)
    boxscore = r_boxscore.json()
    teams = boxscore.get('teams')
    if teams.get('away').get('teamStats'):
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


def get_teams():
    url = 'http://statsapi.mlb.com/api/v1/teams?sportId=1'
    r = requests.get(url)
    teams = r.json().get('teams')
    teams = sorted(teams, key = lambda team: (team['name']))
    team_display = []
    for i in range(len(teams)):
        team_display.append({'id': teams[i].get('id'), 'name': teams[i].get('name')})
    return team_display


def get_form_details(request):
    sportId = 1
    team1 = request.GET.get('team1')
    team2 = request.GET.get('team2')
    teamId = f'{team1},{team2}'
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    params = {
        'sportId': sportId,
        'teamId': teamId,
        'startDate': start_date,
        'endDate': end_date
    }
    url = 'http://statsapi.mlb.com/api/v1/schedule/games'
    r = requests.get(url, params)
    games_dates = r.json().get('dates')
    display_dates = []
    if games_dates is not None:
        for i in range(len(games_dates)):
            date = games_dates[i].get('date')
            for j in range(len(games_dates[i].get('games'))):
                away = games_dates[i].get('games')[j].get('teams').get('away').get('team').get('name')
                away_id = games_dates[i].get('games')[j].get('teams').get('away').get('team').get('id')
                home = games_dates[i].get('games')[j].get('teams').get('home').get('team').get('name')
                home_id = games_dates[i].get('games')[j].get('teams').get('home').get('team').get('id')
                away_score = games_dates[i].get('games')[j].get('teams').get('away').get('score')
                home_score = games_dates[i].get('games')[j].get('teams').get('home').get('score')
                text = f'{date}: {away} vs {home}. Final Score: {away_score} - {home_score}'
                gamePk = games_dates[i].get('games')[j].get('gamePk')
                data = {
                    'text': text,
                    'gamePk': gamePk
                }
                if (str(home_id) == team1 and str(away_id) == team2) or (
                        str(home_id) == team2 and str(away_id) == team1):
                    display_dates.append(data)
    return  display_dates