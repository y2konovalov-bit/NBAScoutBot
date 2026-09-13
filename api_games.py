import requests
import time
from config import BALLDONTLIE_KEYS


BASE_URL = "https://api.balldontlie.io/nba/v1"

def get_games(team_id, schedule_type):
    today = time.strftime('%Y-%m-%d')
    params = {'team_ids[]': team_id, 'per_page': 5}
    if schedule_type == 'upcoming':
        params['start_date'] = today
    else:
        params['end_date'] = today

    headers = {'Authorization': BALLDONTLIE_KEYS[0]}
    try:
        response = requests.get(f'{BASE_URL}/games', params=params, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        return None

    if response.status_code != 200:
        return None

    games_data = response.json()['data']

    result = []
    for game in games_data:
        is_home = game['home_team']['id'] == team_id
        if is_home:
            opponent = game['visitor_team']['name']
            our_score = game['home_team_score']
            their_score = game['visitor_team_score']
        else:
            opponent = game['home_team']['name']
            our_score = game['visitor_team_score']
            their_score = game['home_team_score']
            
        if game['status'] == 'Final':
            score = f"{our_score}:{their_score}"
        else:
            score = None

        result.append({
            'date': game['date'],
            'opponent': opponent,
            'score': score
        })

    if schedule_type == 'past':
        result.reverse()

    return result 

print(get_games(5, 'past'))
    