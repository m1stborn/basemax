import os
import json
from pathlib import Path

import redis

ON_HEROKU = os.environ.get('ON_HEROKU', None)

if ON_HEROKU:
    REDIS_URL = os.environ.get('REDIS_URL', None)
else:
    config = json.loads(Path('./config.json').read_text())
    REDIS_URL = config["REDIS_URL"]

r = redis.from_url(REDIS_URL)


def get_game_data():
    game_infos = json.loads(r.get('games').decode('utf-8'))
    print(game_infos)
    return game_infos


def get_game_title():
    game_infos = json.loads(r.get('games').decode('utf-8'))
    game_titles = {url: f"{game['team_away']}vs{game['team_home']}".strip()
                   for url, game in game_infos.items()}

    return game_titles


def get_broadcast_list(game_url):
    broadcast_list = json.loads(r.get('broadcast_list').decode('utf-8'))

    return broadcast_list[game_url]


def update_broadcast_list(game_url, user_id):
    broadcast_list = json.loads(r.get('broadcast_list').decode('utf-8'))

    if user_id not in broadcast_list[game_url]:
        broadcast_list[game_url].append(user_id)

    print(broadcast_list)

    r.set("broadcast_list", json.dumps(broadcast_list))


def update_games_data(games_infos):
    r.set("games", json.dumps(games_infos))


def init_data(game_infos):
    games_uid = [url for url, game in game_infos.items()]
    empty_broadcast_list = {url: [] for url, game in game_infos.items()}

    if r.exists("broadcast_list"):
        current_broadcast_list = json.loads(r.get("broadcast_list").decode('utf-8'))
        if games_uid[0] not in current_broadcast_list:
            r.set("broadcast_list", json.dumps(empty_broadcast_list))

    # for uid in games_uid:
    # r.set(f"{uid}_broadcast_list", json.dumps([]))

    r.set("games_uid", json.dumps(games_uid))
    r.set("games", json.dumps(game_infos))

    print("Redis:", json.loads(r.get("games_uid").decode('utf-8')))
    print("Redis:", json.loads(r.get("games").decode('utf-8')))
    print("Redis:", json.loads(r.get("broadcast_list").decode('utf-8')))
