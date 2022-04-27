import os
import json
from pathlib import Path

import redis

ON_HEROKU = os.environ.get('ON_HEROKU', None)

if ON_HEROKU:
    REDIS_URL = os.environ.get('REDIS_URL', None)
else:
    config = json.loads(Path('config.json').read_text())
    REDIS_URL = config["REDIS_URL"]

print(REDIS_URL)
r = redis.from_url(REDIS_URL)


def get_game_data():
    # game_infos = json.loads(Path("games.json").read_text(encoding="utf-8"))
    game_infos = json.loads(r.get('games').decode('utf-8'))
    return game_infos


def get_game_title():
    # game_infos = json.loads(Path("games.json").read_text(encoding="utf-8"))
    game_infos = json.loads(r.get('games').decode('utf-8'))
    game_titles = {url: f"{game['team_away']}vs{game['team_home']}".strip()
                   for url, game in game_infos.items()}

    return game_titles


def update_broadcast_list(game_url, user_id):
    # broadcast_list = json.loads(Path("broadcast_list.json").read_text(encoding="utf-8"))
    broadcast_list = json.loads(r.get('broadcast_list').decode('utf-8'))

    if user_id not in broadcast_list[game_url]:
        broadcast_list[game_url].append(user_id)

    with open('broadcast_list.json', 'w', encoding="utf-8") as f:
        json.dump(broadcast_list, f, indent=4, ensure_ascii=False)


def get_broadcast_list(game_url):
    broadcast_list = json.loads(r.get('broadcast_list').decode('utf-8'))
    # users_to_broadcast = json.loads(Path("broadcast_list.json").read_text(encoding="utf-8"))

    return broadcast_list[game_url]
