import os
import json
from pathlib import Path

from typing import Dict, List

from schemas.standing import Team
from models import game_mod
from line.footer_flex import footer_flex

ON_HEROKU = os.environ.get('ON_HEROKU', None)
if ON_HEROKU:
    LIFF_ID = os.getenv('LIFF_SHARE_ID')
else:
    config = json.loads(Path('./config.json').read_text())
    LIFF_ID = config["LIFF_SHARE_ID"]

CPBL_URL = "https://www.cpbl.com.tw"
SHARE_STANDING_URL = f"https://liff.line.me/{LIFF_ID}/standing"

team_name_map = {
    '樂天桃猿': '樂天桃猿',
    '中信兄弟': '中信兄弟',
    '味全龍': '味全龍',
    '統一7-ELEVEn獅': '統一獅',
    '富邦悍將': '富邦悍將'
}

team_logo_map = {
    '樂天桃猿': "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_monkeys.png",
    '中信兄弟': "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_brothers.png",
    '味全龍': "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_dragon.png",
    '統一7-ELEVEn獅': "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_lions.png",
    '富邦悍將': "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/logo_fubon.png"
}


def team_row_flex(team: Team) -> Dict:
    return {
        "type": "box",
        "layout": "horizontal",
        "margin": "md",
        "contents": [
            {
                "type": "text",
                "text": team.ranking,
                "flex": 2,
                "align": "start",
                "size": "sm",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": team_name_map[team.team],
                "size": "sm",
                "color": "#555555",
                "align": "start",
                "gravity": "center",
                "weight": "bold",
                "flex": 5
            },
            {
                "type": "text",
                "text": team.win,
                "size": "sm",
                "color": "#111111",
                "align": "center",
                "gravity": "center",
                "flex": 2
            },
            {
                "type": "text",
                "text": team.tie,
                "size": "sm",
                "color": "#111111",
                "align": "center",
                "gravity": "center",
                "flex": 2
            },
            {
                "type": "text",
                "text": team.lose,
                "size": "sm",
                "color": "#111111",
                "gravity": "center",
                "flex": 2,
                "align": "center"
            },
            {
                "type": "text",
                "text": team.win_rate,
                "size": "sm",
                "color": "#111111",
                "align": "center",
                "gravity": "center",
                "flex": 3
            },
            {
                "type": "text",
                "text": team.game_behind,
                "size": "sm",
                "color": "#111111",
                "align": "center",
                "gravity": "center",
                "flex": 3
            },
            {
                "type": "image",
                "gravity": "center",
                "url": team_logo_map[team.team],
                "flex": 2,
                "aspectMode": "fit",
                "align": "center"
            }
        ],
        "spacing": "none"
    }


def standing_flex(title: str, teams: List[Team]) -> Dict:
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Standing",
                    "weight": "bold",
                    "align": "start",
                    "color": "#9FA8DA",
                    "margin": "md",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": title,
                    "color": "#303F9F",
                    "size": "xl",
                    "gravity": "center",
                    "margin": "md"
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
                                    "text": "R",
                                    "flex": 2,
                                    "color": "#9FA8DA",
                                    "size": "sm",
                                    "weight": "bold",
                                    "align": "start"
                                },
                                {
                                    "type": "text",
                                    "text": "Team",
                                    "size": "sm",
                                    "color": "#9FA8DA",
                                    "weight": "bold",
                                    "flex": 5,
                                    "align": "start"
                                },
                                {
                                    "type": "text",
                                    "text": "W",
                                    "size": "sm",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "T",
                                    "size": "sm",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "L",
                                    "size": "sm",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": "%",
                                    "size": "sm",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 3
                                },
                                {
                                    "type": "text",
                                    "text": "GB",
                                    "size": "sm",
                                    "color": "#9FA8DA",
                                    "align": "center",
                                    "weight": "bold",
                                    "flex": 3
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "flex": 2
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "color": "#9FA8DA"
                        },
                        *[team_row_flex(team) for team in teams],
                        {
                            "type": "separator",
                            "color": "#9FA8DA"
                        }
                    ]
                }
            ]
        },
        # "footer": footer_flex(BASE_URL, BASE_URL) if footer else None,
    }


def standing_content(footer: bool = True):
    title, teams = game_mod.get_standings()
    flex = standing_flex(title, teams)
    if footer:
        flex["footer"] = footer_flex(CPBL_URL, SHARE_STANDING_URL)
    return flex

