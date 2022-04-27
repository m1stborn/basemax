import re
import time
import json
import multiprocessing as mp
from typing import List, Dict, Union
import warnings
from pathlib import Path
from datetime import date

import schedule
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from linebot.models import (
    FlexSendMessage,
)

warnings.filterwarnings("ignore")


def flex_message_type_condition(alt: str, contents: list or dict, **kwargs):
    if type(contents) == list:
        output_flex_message = {
            "type": "carousel",
            "contents": contents
        }
    else:
        output_flex_message = contents
    return FlexSendMessage(
        alt,
        output_flex_message,
        **kwargs
    )


def game_flex(game_info):
    team_away = game_info["team_away"]
    team_home = game_info["team_home"]
    baseball_field = game_info["baseball_field"]
    game_time = game_info["game_time"]
    try:
        current_score = game_info["current_score"]
    except KeyError:
        current_score = "0:0"

    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": team_away,
                    "align": "center",
                    "gravity": "center"
                },
                {
                    "type": "text",
                    "text": "VS",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": team_home
                }
            ]
        },
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": current_score,
                    "align": "center",
                    "gravity": "center",
                    "size": "xxl"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": baseball_field,
                    "gravity": "center",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": game_time,
                    "align": "center",
                    "gravity": "center"
                }
            ]
        }
    }


def today_game():
    game_infos = json.loads(Path("games.json").read_text(encoding="utf-8"))

    contents = [game_flex(game) for url, game in game_infos.items()]
    return contents


# # Redis manipulate
# def get_game_data():
#     game_infos = json.loads(Path("games.json").read_text(encoding="utf-8"))
#
#     return game_infos
#
#
# def get_game_title():
#     game_infos = json.loads(Path("games.json").read_text(encoding="utf-8"))
#     game_titles = [f"{game['team_away']}vs{game['team_home']}".strip() for url, game in game_infos.items()]
#
#     return game_titles
#
#
# def update_broadcast_list(user_id):
#     users_to_broadcast = json.loads(Path("../broadcast_list.json").read_text(encoding="utf-8"))
#     if user_id not in users_to_broadcast:
#         users_to_broadcast.append(user_id)
#
#     with open('../broadcast_list.json', 'w', encoding="utf-8") as f:
#         json.dump(users_to_broadcast, f, indent=4, ensure_ascii=False)
