import os
import json
import logging
from pathlib import Path
from typing import Dict, List

import redis

from schemas.game import Game, GameState

logger = logging.getLogger(__name__)

ON_HEROKU = os.environ.get('ON_HEROKU', None)
if ON_HEROKU:
    REDIS_URL = os.environ.get('REDIS_URL', None)
else:
    config = json.loads(Path('./config.json').read_text())
    REDIS_URL = config["REDIS_URL"]

r = redis.from_url(REDIS_URL)


def get_games_info() -> Dict[str, Game]:
    games_json = json.loads(r.get('games').decode('utf-8'))
    games = {k: Game(**game) for k, game in games_json.items()}
    return games


def get_game_title() -> Dict[str, str]:
    games_json = json.loads(r.get('games').decode('utf-8'))
    games = {k: Game(**game) for k, game in games_json.items()}
    game_titles = {url: f"{game.team_away}vs{game.team_home}".strip()
                   for url, game in games.items()}
    return game_titles


def get_broadcast_list(game_uid: str) -> List[str]:
    broadcast_list = json.loads(r.get('broadcast_list').decode('utf-8'))
    return broadcast_list[game_uid]


def get_game_state(game_uid: str) -> GameState:
    game_state_json = json.loads(r.get('games_state').decode('utf-8'))
    game_state = GameState(**game_state_json[game_uid])
    return game_state


def get_game_states() -> Dict[str, GameState]:
    game_state_json = json.loads(r.get('games_state').decode('utf-8'))
    game_state = {url: GameState(**game) for url, game in game_state_json.items()}
    return game_state


def update_broadcast_list(game_uid: str, user_id: str):
    broadcast_list = json.loads(r.get('broadcast_list').decode('utf-8'))
    if game_uid not in broadcast_list:
        broadcast_list[game_uid] = []

    if user_id not in broadcast_list[game_uid]:
        broadcast_list[game_uid].append(user_id)

    r.set("broadcast_list", json.dumps(broadcast_list))


def update_games_data(games: Dict[str, Game]):
    r.set("games", json.dumps(games, default=vars, ensure_ascii=False))


def update_one_game_data(games: Game):
    games_json = json.loads(r.get("games").decode('utf-8'))
    # games[game_info.game_url_postfix] = {**vars(game_info)}
    # r.set("games", json.dumps(games_json, default=vars, ensure_ascii=False))

    game_infos = {k: Game(**game) for k, game in games_json.items()}
    game_infos[games.game_url_postfix] = games
    r.set("games", json.dumps(game_infos, default=vars, ensure_ascii=False))


def update_one_game_state(game_uid: str, game_state: GameState):
    games_state = json.loads(r.get("games_state").decode('utf-8'))
    games_state[game_uid] = {**vars(game_state)}

    r.set("games_state", json.dumps(games_state, default=vars, ensure_ascii=False))


def init_data(games):
    games_uid = [url for url, game in games.items()]
    empty_broadcast_list = {url: [] for url, game in games.items()}
    empty_games_state = {url: {} for url, game in games.items()}

    if r.exists("broadcast_list"):
        current_broadcast_list = json.loads(r.get("broadcast_list").decode('utf-8'))
        if games_uid[0] not in current_broadcast_list:
            r.set("broadcast_list", json.dumps(empty_broadcast_list))

    r.set("games_uid", json.dumps(games_uid))
    r.set("games", json.dumps(games, default=vars, ensure_ascii=False))
    r.set("games_state", json.dumps(empty_games_state))

    logger.info(f"Init Redis game_uid = {json.loads(r.get('games_uid').decode('utf-8'))}")
    logger.info(f"Init Redis games = {json.loads(r.get('games').decode('utf-8'))}")
    logger.info(f"Init Redis broadcast_list = {json.loads(r.get('broadcast_list').decode('utf-8'))}")
    logger.info(f"Init Redis games_state = {json.loads(r.get('games_state').decode('utf-8'))}")
