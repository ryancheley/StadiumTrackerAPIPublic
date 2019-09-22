from datetime import datetime
import requests


def get_game_object(game_id):
    game_url = f'http://statsapi.mlb.com/api/v1/schedule/games?sportId=1&gamePk={game_id}'
    game = requests.get(game_url)
    return game

def get_game_story(game_id):
    story_url = f'http://statsapi.mlb.com/api/v1/game/{game_id}/content'
    story = requests.get(story_url)
    return story

def get_game_date(game_id):
    v = get_game_object(game_id).json().get('dates')[0].get('date')
    return v

def get_game_recap(game_id, type):
    story = get_game_story(game_id)
    if story.status_code==200:
        recap = story.json().get('editorial').get('recap').get('mlb')
        if recap is not None:
            data = recap.get(f'{type}')
        return data

def get_venue_id(game_id):
    v = get_game_object(game_id).json().get('dates')[0].get('games')[0].get('venue').get('id')
    return v

def get_boxscore(game_id, type):
    boxscore_url = f'http://statsapi.mlb.com/api/v1/game/{game_id}/boxscore'
    r_boxscore = requests.get(boxscore_url)
    boxscore = r_boxscore.json()
    teams = boxscore.get('teams')
    if len(boxscore.get('teams').get('home').get('teamStats')) > 0:
        team = {
            'hits': teams.get(f'{type}').get('teamStats').get('batting').get('hits'),
            'runs': teams.get(f'{type}').get('teamStats').get('batting').get('runs'),
            'errors': teams.get(f'{type}').get('teamStats').get('fielding').get('errors'),
            'team': teams.get(f'{type}').get('team').get('name'),
        }
    else:
        team = None
    return team

def get_score(sportId, gamePk, type):
    params = {
        'sportId': sportId,
        'gamePk': gamePk,
    }
    url = 'http://statsapi.mlb.com/api/v1/schedule/games'
    r = requests.get(url, params)
    score = None
    if r.json().get('dates'):
        games_date = r.json().get('dates')[0].get('date')
        home_team_id = r.json().get('dates')[0].get('games')[0].get('teams').get('home').get('team').get('id')
        away_team_id = r.json().get('dates')[0].get('games')[0].get('teams').get('away').get('team').get('id')
        teamId = f'{home_team_id},{away_team_id}'
        params2 = {
            'sportId': sportId,
            'teamId': teamId,
            'startDate': games_date,
            'endDate': games_date,
        }
        r2 = requests.get(url, params2)
        score = r2.json().get('dates')[0].get('games')[0].get('teams').get(f'{type}').get('score')
    return score


def get_teams() -> list:
    """
    :return: list of teams in alphabetical order
    """
    url = 'http://statsapi.mlb.com/api/v1/teams?sportId=1'
    r = requests.get(url)
    teams = r.json().get('teams')
    teams = sorted(teams, key = lambda team: (team['name']))
    team_display = []
    for i in range(len(teams)):
        team_display.append({'id': teams[i].get('id'), 'name': teams[i].get('name')})
    return team_display


def get_form_details(request):
    """

    :param request: the request object from the page
    :return: list of dictionaries
        text: String of Game
        gamePk: Int of the gamePk
    """
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
                venue_id = games_dates[i].get('games')[j].get('venue').get('id')
                data = {
                    'text': text,
                    'gamePk': gamePk,
                    'venue_id': venue_id
                }
                if (str(home_id) == team1 and str(away_id) == team2) or (
                        str(home_id) == team2 and str(away_id) == team1):
                    display_dates.append(data)
    return display_dates
