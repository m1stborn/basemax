import json
from pathlib import Path


def get_game_data():
    game_infos = json.loads(Path("games.json").read_text(encoding="utf-8"))

    return game_infos


def get_game_title():
    game_infos = json.loads(Path("games.json").read_text(encoding="utf-8"))
    game_titles = {url: f"{game['team_away']}vs{game['team_home']}".strip()
                   for url, game in game_infos.items()}

    return game_titles


def update_broadcast_list(game_url, user_id):
    users_to_broadcast = json.loads(Path("broadcast_list.json").read_text(encoding="utf-8"))

    if user_id not in users_to_broadcast[game_url]:
        users_to_broadcast[game_url].append(user_id)

    with open('broadcast_list.json', 'w', encoding="utf-8") as f:
        json.dump(users_to_broadcast, f, indent=4, ensure_ascii=False)


def get_broadcast_list(game_url):
    users_to_broadcast = json.loads(Path("broadcast_list.json").read_text(encoding="utf-8"))

    return users_to_broadcast[game_url]
