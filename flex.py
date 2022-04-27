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

image_url = {
    " 中信兄弟 ": "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_brothers_large.png",
    " 味全龍 ": "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_dragon_large.png",
    " 富邦悍將 ": "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_fubon_large.png",
    " 統一7-ELEVEn獅 ": "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_lions_large.png",
    " 樂天桃猿 ": "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_monkeys_large.png"
}


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

    team_away_image = image_url[team_away]
    team_home_image = image_url[team_home]

    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "image",
                            "url": team_away_image
                        },
                        {
                            "type": "text",
                            "text": team_away,
                            "size": "lg",
                            "weight": "bold"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": "vs",
                    "align": "center",
                    "gravity": "center",
                    "style": "italic",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "image",
                            "url": team_home_image
                        },
                        {
                            "type": "text",
                            "text": team_home,
                            "size": "lg",
                            "weight": "bold"
                        }
                    ]
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
                    "weight": "bold",
                    "size": "xxl"
                }
            ],
            "flex": 0
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": baseball_field,
                    "weight": "bold",
                    "align": "center",
                    "gravity": "center"
                },
                {
                    "type": "text",
                    "text": game_time,
                    "weight": "bold",
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
