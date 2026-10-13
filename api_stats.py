import requests
import logging
from storage import load_cache, save_cache
from config import NBA_STATS_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://v2.nba.api-sports.io"

STANDINGS_CACHE_FILE = 'standings_cache.json'
PLAYER_STATS_CACHE_FILE = 'player_stats_cache.json'


def get_standings(season, view_type='all'):
    """Получает турнирную таблицу с кэшированием."""
    cached = load_cache(STANDINGS_CACHE_FILE, max_age_hours=6)
    if cached is not None:
        logger.info("Используется кэшированная таблица")
        return cached

    headers = {"x-apisports-key": NBA_STATS_KEY}
    params = {"league": "standard", "season": season}

    try:
        logger.info(f"Запрос к API: {BASE_URL}/standings с params {params}")
        response = requests.get(
            f"{BASE_URL}/standings",
            params=params,
            headers=headers,
            timeout=10
        )
        logger.info(f"Ответ от API: статус {response.status_code}")
    except requests.exceptions.Timeout:
        logger.error("Timeout: API не ответил за 10 секунд")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("ConnectionError: не удалось подключиться к API")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса: {e}")
        return None

    if response.status_code == 429:
        logger.warning("Лимит запросов исчерпан (429)")
        return None
    if response.status_code >= 500:
        logger.error(f"Сервер API вернул ошибку: {response.status_code}")
        return None
    if response.status_code != 200:
        logger.error(f"API вернул статус {response.status_code}, ожидалось 200")
        return None

    try:
        data = response.json().get('response', [])
    except ValueError as e:
        logger.error(f"Ошибка при парсинге JSON: {e}")
        return None

    standings = []
    for s in data[:10]:
        team = s.get('team', {})
        standings.append({
            'name': team.get('name', 'Неизвестно'),
            'wins': s.get('win', {}).get('total', 0),
            'losses': s.get('loss', {}).get('total', 0)
        })

    logger.info(f"Сохранена таблица с {len(standings)} командами")
    save_cache(STANDINGS_CACHE_FILE, standings)
    return standings

def find_player(player_name):
    """Ищет игрока в balldontlie."""
    from config import BALLDONTLIE_KEYS
    
    headers = {"Authorization": BALLDONTLIE_KEYS[0]}
    params = {"search": player_name}

    try:
        logger.info(f"Поиск в balldontlie: {player_name}")
        response = requests.get(
            "https://api.balldontlie.io/nba/v1/players",
            params=params,
            headers=headers,
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при поиске: {e}")
        return None

    if response.status_code != 200:
        logger.error(f"balldontlie вернул {response.status_code}")
        return None

    data = response.json().get('data', [])
    if not data:
        logger.info(f"Игрок '{player_name}' не найден")
        return None

    player_id = data[0].get('id')
    player_name_full = f"{data[0].get('first_name', '')} {data[0].get('last_name', '')}"
    logger.info(f"Найден в balldontlie: {player_name_full}")
    
    return {"id": player_id, "name": player_name_full}


def get_player_stats(player_id, season):
    """Получает базовую информацию об игроке из balldontlie."""
    headers = {"Authorization": BALLDONTLIE_KEYS[0]}

    try:
        response = requests.get(
            f"https://api.balldontlie.io/nba/v1/players/{player_id}",
            headers=headers,
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка: {e}")
        return None

    if response.status_code != 200:
        return None

    player = response.json()['data']
    
    return {
        'name': f"{player.get('first_name', '')} {player.get('last_name', '')}",
        'height': player.get('height_feet', 'неизвестно'),
        'weight': player.get('weight_pounds', 'неизвестно'),
        'position': player.get('position', 'неизвестно'),
        'team': player.get('team', {}).get('name', 'неизвестно'),
    }

# def find_player(player_name):
#     """Ищет игрока по имени, возвращает его id."""
#     headers = {"x-apisports-key": NBA_STATS_KEY}
#     params = {"search": player_name}

#     try:
#         logger.info(f"Поиск игрока: {player_name}")
#         response = requests.get(
#             f"{BASE_URL}/players",
#             params=params,
#             headers=headers,
#             timeout=10
#         )
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Ошибка при поиске игрока: {e}")
#         return None

#     if response.status_code != 200:
#         logger.error(f"API вернул {response.status_code} при поиске игрока")
#         return None

#     data = response.json().get('response', [])
#     if not data:
#         logger.info(f"Игрок '{player_name}' не найден")
#         return None

#     player_id = data[0].get('id')
#     logger.info(f"Найден игрок ID: {player_id}")
#     return player_id


# def get_player_stats(player_id, season):
#     """Получает статистику игрока с кэшированием."""
#     # cached = load_cache(PLAYER_STATS_CACHE_FILE, max_age_hours=12)
#     # if cached is not None:
#     #     logger.info("Используется кэшированная статистика")
#     #     return cached

#     headers = {"x-apisports-key": NBA_STATS_KEY}
#     params = {"id": player_id, "season": season}

#     try:
#         logger.info(f"Запрос статистики игрока ID {player_id}")
#         response = requests.get(
#             f"{BASE_URL}/players/statistics",
#             params=params,
#             headers=headers,
#             timeout=10
#         )
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Ошибка при получении статистики: {e}")
#         return None

#     if response.status_code == 429:
#         logger.warning("Лимит запросов исчерпан (429)")
#         return None
#     if response.status_code != 200:
#         logger.error(f"API вернул {response.status_code}")
#         return None

#     data = response.json().get('response', [])
#     if not data:
#         logger.error(f"Нет данных для игрока ID {player_id}")
#         return None

#     player_data = data[0]
#     player_name = f"{player_data.get('player', {}).get('firstname', '')} {player_data.get('player', {}).get('lastname', '')}"
#     stats = player_data.get('statistics', [{}])[0]

#     logger.info(f"Реальная структура stats: {stats}")
    
#     result = {
#         'name': player_name,
#         'points': stats.get('points') or stats.get('pts') or 0,
#         'rebounds': stats.get('totRebounds') or stats.get('reb') or stats.get('rebounds') or 0,
#         'assists': stats.get('assists') or stats.get('ast') or 0,
#         'games_played': stats.get('gamesPlayed') or stats.get('games') or 0,
#     }

#     logger.info(f"Сохранена статистика {player_name}: {result}")
#     save_cache(PLAYER_STATS_CACHE_FILE, result)
#     return result

