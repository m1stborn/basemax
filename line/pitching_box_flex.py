from datetime import datetime
from typing import Dict, List, Union
from urllib.parse import urlencode

from line.footer_flex import footer_flex
from schemas.game import GameBox
from schemas.player import Batter, Pitcher
from models import game_cache


def pitcher_row_flex(pitcher: Pitcher) -> Dict:
    return {
        "type": "box",
        "layout": "horizontal",
        "margin": "md",
        "contents": [
            {
                "type": "text",
                "text": pitcher.name,
                "flex": 4,
                "size": "xxs"
            },
            {
                "type": "text",
                "text": pitcher.ip,
                "flex": 2,
                "align": "start",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": pitcher.pc,
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": pitcher.hit,
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": pitcher.run,
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": pitcher.er,
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": pitcher.bb,
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": pitcher.k,
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": pitcher.era,
                "flex": 3,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": pitcher.whip,
                "flex": 3,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            }
        ],
        "spacing": "none"
    }


def pitching_box_flex(title: str, team_name, pitchers: List[Pitcher]) -> Dict:
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "align": "start",
                    "color": "#082568",
                    "margin": "md",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "color": "#303F9F",
                    "size": "xl",
                    "gravity": "center",
                    "margin": "md",
                    "text": team_name
                },
                {
                    "type": "separator",
                    "color": "#9FA8DA"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "投手",
                                    "flex": 4,
                                    "color": "#9FA8DA",
                                    "weight": "bold",
                                    "align": "start",
                                    "size": "xxs"
                                },
                                {
                                    "type": "text",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "weight": "bold",
                                    "flex": 2,
                                    "align": "start",
                                    "text": "IP"
                                },
                                {
                                    "type": "text",
                                    "text": "PC",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "H",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "R",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "ER",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "BB",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "K",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "ERA",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 3
                                },
                                {
                                    "type": "text",
                                    "text": "WHIP",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 3
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "color": "#9FA8DA"
                        },
                        *[pitcher_row_flex(pitcher) for pitcher in pitchers],
                        {
                            "type": "separator",
                            "color": "#9FA8DA"
                        }
                    ]
                }
            ]
        }
    }


def pitching_box_contents(game_uid: str, footer: bool = True) -> List:
    game_box = game_cache.get_game_box(game_uid)
    if game_box.home_pitch_box is None:
        return []
    title = f"{game_box.game_time_int} {game_box.game_title}"
    home_flex = pitching_box_flex(title=title,
                                  team_name=game_box.game_title.split("vs")[1].strip(),
                                  pitchers=game_box.home_pitch_box)
    away_flex = pitching_box_flex(title=title,
                                  team_name=game_box.game_title.split("vs")[0].strip(),
                                  pitchers=game_box.away_pitch_box)
    contents = [away_flex, home_flex]
    if footer:
        query_string = {
            'gameSno': game_uid.split("&")[-1].split("=")[-1]
        }
        for flex in contents:
            flex["footer"] = footer_flex(post_fix=f"/pitchbox?{urlencode(query_string)}")

    return contents
