import json

SUBSCRIPTIONS_FILE = "subscriptions.json"

def load_json(file_name, default=None):
    if default is None:
        default = {}
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f) # десериализация
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_user_team(user_id, team_name):
    data = load_json(SUBSCRIPTIONS_FILE)
    user_key = str(user_id)
    teams = data.get(user_key, [])
    
    if team_name in teams:
        return False
    
    teams.append(team_name)
    data[user_key] = teams
    save_json(SUBSCRIPTIONS_FILE, data)
    return True


def delete_user_team(user_id, team_name):
    data = load_json(SUBSCRIPTIONS_FILE)
    user_key = str(user_id)
    teams = data.get(user_key, [])
    
    if team_name not in teams:
        return False
    
    teams.remove(team_name)
    data[user_key] = teams
    save_json(SUBSCRIPTIONS_FILE, data)
    return True


def load_user_teams(user_id):
    data = load_json(SUBSCRIPTIONS_FILE)
    return data.get(str(user_id), [])
