import os
import json
import logging
from pathlib import Path
from typing import Dict, List

import redis

from schemas.game import Game, GameState, GameBox
from schemas.standing import Team
from config import Setting

logger = logging.getLogger(__name__)
setting = Setting()

r = redis.from_url(setting.REDIS_URL)


def get_games_info() -> Dict[str, Game]:
    games_json = json.loads(r.get('games').decode('utf-8'))
    games = {k: Game(**game) for k, game in games_json.items()}
    return games


short_team_name = {
    "中信兄弟": "中信",
    "味全龍": "味全",
    "富邦悍將": "富邦",
    "統一7-ELEVEn獅": "統一",
    "樂天桃猿": "樂天",
}


def get_game_title() -> Dict[str, str]:
    games_json = json.loads(r.get('games').decode('utf-8'))
    games = {k: Game(**game) for k, game in games_json.items()}
    # TODO: make short team name Game' s attribute
    game_titles = {url: f"{short_team_name[game.team_away]}vs{short_team_name[game.team_home]}".strip()
                   for url, game in games.items() if "延賽" not in game.game_time}
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
    game_state = {url: GameState(**game)
                  for url, game in game_state_json.items() if game != {}}
    return game_state


def get_standing_by_season(title: str = "2022年 上半季") -> List[Team]:
    standings_json = json.loads(r.get('standings').decode('utf-8'))
    teams = standings_json.get(title, None)

    if teams is None:
        return []

    teams = [Team(**team) for team in teams["teams"]]
    return teams


def get_standings() -> (Dict[str, List[Team]]):
    standings_json = json.loads(r.get('standings').decode('utf-8'))

    return {title: [Team(**team) for team in teams]
            for title, teams in standings_json.items()}


def update_standings(title: str, teams: List[Team]):
    standings_json = json.loads(r.get('standings').decode('utf-8'))
    standings_json[title] = teams

    r.set('standings', json.dumps(standings_json, default=vars, ensure_ascii=False))


# def tmp_set():
#     standings_json = json.loads(r.get('standings').decode('utf-8'))
#     _ = standings_json.pop("title", None)
#     _ = standings_json.pop("teams", None)
#     r.set('standings', json.dumps(standings_json, default=vars, ensure_ascii=False))


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


def update_game_box(game_uid: str, game_box: GameBox):
    games_box_score = json.loads(r.get("games_box").decode('utf-8'))
    games_box_score[game_uid] = {**vars(game_box)}

    r.set("games_box", json.dumps(games_box_score, default=vars, ensure_ascii=False))


def get_game_box(game_uid: str) -> GameBox:
    game_box_json = json.loads(r.get('games_box').decode('utf-8'))
    game_box = {k: GameBox(**box) for k, box in game_box_json.items()}
    return game_box[game_uid]


def get_game_boxes() -> Dict[str, GameBox]:
    game_box_json = json.loads(r.get('games_box').decode('utf-8'))
    game_box = {k: GameBox(**box) for k, box in game_box_json.items()}
    return game_box


def init_data(games):
    games_uid = [url for url, game in games.items()]
    empty_broadcast_list = {url: [] for url, game in games.items()}
    empty_games_state = {url: {} for url, game in games.items()}
    empty_box_score = {url: {} for url, game in games.items()}

    if r.exists("broadcast_list"):
        current_broadcast_list = json.loads(r.get("broadcast_list").decode('utf-8'))
        logger.info(f"{games_uid}")
        if games_uid[0] not in current_broadcast_list:
            r.set("broadcast_list", json.dumps(empty_broadcast_list))
    else:
        r.set("broadcast_list", json.dumps(empty_broadcast_list))

    r.set("games_uid", json.dumps(games_uid))
    r.set("games", json.dumps(games, default=vars, ensure_ascii=False))
    r.set("games_state", json.dumps(empty_games_state))
    r.set("games_box", json.dumps(empty_box_score))

    logger.info(f"Init Redis game_uid = {json.loads(r.get('games_uid').decode('utf-8'))}")
    logger.info(f"Init Redis games = {json.loads(r.get('games').decode('utf-8'))}")
    logger.info(f"Init Redis broadcast_list = {json.loads(r.get('broadcast_list').decode('utf-8'))}")
    logger.info(f"Init Redis games_state = {json.loads(r.get('games_state').decode('utf-8'))}")
