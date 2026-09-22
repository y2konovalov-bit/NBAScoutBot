import requests
from datetime import date, timedelta
from config import BALLDONTLIE_KEYS


BASE_URL = "https://api.balldontlie.io/nba/v1"

key_index = 0

def get_next_key():
    global key_index
    key = BALLDONTLIE_KEYS[key_index % len(BALLDONTLIE_KEYS)]
    key_index += 1
    return key    

def get_games(team_id, schedule_type):
    today = date.today()
    params = {'team_ids[]': team_id} # 'per_page': 10
    if schedule_type == 'upcoming':
        params['start_date'] = today
        params['per_page'] = 10
    else:
        params['start_date'] = (today - timedelta(days=160)).strftime('%Y-%m-%d')
        params['end_date'] = today
        params['per_page'] = 100

    headers = {'Authorization': get_next_key()}
    try:
        response = requests.get(f'{BASE_URL}/games', params=params, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        return None

    if response.status_code != 200:
        return None

    games_data = response.json()['data']

    if schedule_type == 'past':
        games_data = games_data[-10:]

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