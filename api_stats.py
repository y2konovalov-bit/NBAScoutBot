import requests
import logging #
from storage import load_cache, save_cache
from config import NBA_STATS_KEY

logging.basicConfig(level=logging.INFO) #
logger = logging.getLogger(__name__) #

BASE_URL = "https://v2.nba.api-sports.io"

STANDINGS_CACHE_FILE = 'standings_cache.json'
PLAYER_STATS_CACHE_FILE = 'player_stats_cache.json'


def get_standings(season, view_type='all'):
    cached = load_cache(STANDINGS_CACHE_FILE)
    if cached is not None:
        return cached

    headers = {"x-apisports-key": NBA_STATS_KEY}
    params = {"league": "nba", "season": season}

    try:
        response = requests.get(f"{BASE_URL}/standings", params=params, headers=headers, timeout=100)
    except requests.exceptions.RequestException:
        logger.error("Timeout при запросе к API") #
        return None # error
    except requests.exceptions.ConnectionError: #
        logger.error("ConnectionError при запросе к API")#
        return None#
    except requests.exceptions.RequestException as e:#
        logger.exception("Общая ошибка запроса: %s", e)#
        return None#

    if response.status_code == 429:
        return None
    if response.status_code >= 500:
        return None
    if response.status_code != 200:
        return None

    data = response.json().get('response', [])

    standings = []
    for s in data[:10]:
        team = s.get('team', {})
        standings.append({
            'name': team.get('name', 'Неизвестно'),
            'wins': s.get('win', {}).get('total', 0),
            'losses': s.get('loss', {}).get('total', 0)
        })
        
    save_cache(STANDINGS_CACHE_FILE, standings)
    return standings

def find_player(player_name):
    pass

def get_player_stats(player_id, season):
    pass

print(get_standings(2024))