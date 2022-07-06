from datetime import datetime
from typing import Dict, List, Union
from urllib.parse import urlencode

from line.footer_flex import footer_flex
from schemas.game import GameBox
from schemas.player import Batter
from models import game_cache


def batter_row_flex(batter: Batter) -> Dict:
    return {
        "type": "box",
        "layout": "horizontal",
        "margin": "md",
        "contents": [
            {
                "type": "text",
                "text": f"{batter.num if batter.num != '' else ' '}{batter.name}",
                "flex": 4,
                "size": "xxs"
            },
            {
                "type": "text",
                "text": f"{batter.pos}",
                "flex": 3,
                "size": "xxs",
                "color": "#DCDFE5"
            },
            {
                "type": "text",
                "text": f"{batter.at_bat}",
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": f"{batter.run}",
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": f"{batter.hit}",
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": f"{batter.rbi}",
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": f"{batter.bb}",
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": f"{batter.so}",
                "flex": 2,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": f"{batter.avg}",
                "flex": 3,
                "align": "center",
                "size": "xxs",
                "gravity": "center"
            }
        ],
        "spacing": "none"
    }


def bat_box_flex(title: str, team_name, batters: List[Batter]) -> Dict:
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"{title}",
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
                    "text": f"{team_name}"
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
                                    "text": "打者",
                                    "flex": 7,
                                    "color": "#9FA8DA",
                                    "size": "xxs",
                                    "weight": "bold",
                                    "align": "start"
                                },
                                {
                                    "type": "text",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "weight": "bold",
                                    "flex": 2,
                                    "align": "center",
                                    "text": "AB"
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
                                    "text": "H",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "RBI",
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
                                    "text": "SO",
                                    "size": "xxs",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "AVG",
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
                        *[batter_row_flex(batter) for batter in batters],
                        {
                            "type": "separator",
                            "color": "#9FA8DA"
                        }
                    ]
                }
            ]
        },
    }


def batting_box_contents(game_uid: str, footer: bool = True) -> List:
    game_box = game_cache.get_game_box(game_uid)
    if game_box.home_bat_box is None:
        return []
    title = f"{game_box.game_time_int} {game_box.game_title}"
    home_flex = bat_box_flex(title=title,
                             team_name=game_box.game_title.split("vs")[1].strip(),
                             batters=game_box.home_bat_box)
    away_flex = bat_box_flex(title=title,
                             team_name=game_box.game_title.split("vs")[0].strip(),
                             batters=game_box.away_bat_box)
    contents = [away_flex, home_flex]
    if footer:
        query_string = {
            'gameSno': game_uid.split("&")[-1].split("=")[-1]
        }
        for flex in contents:
            flex["footer"] = footer_flex(post_fix=f"/batbox?{urlencode(query_string)}")

    return contents
