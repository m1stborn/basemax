from typing import Dict, List

from flask import url_for

from schemas.standing import Team
from models import game_cache
from line.footer_flex import footer_flex, share_footer_flex
from config import Setting


settings = Setting()

team_name_map = {
    '樂天桃猿': '樂天桃猿',
    '中信兄弟': '中信兄弟',
    '味全龍': '味全龍',
    '統一7-ELEVEn獅': '統一獅',
    '富邦悍將': '富邦悍將'
}

logo_small_url = {
    '樂天桃猿': f"{settings.API_BASE}/static/logo/logo_monkeys.png",
    '中信兄弟': f"{settings.API_BASE}/static/logo/logo_brothers.png",
    '味全龍': f"{settings.API_BASE}/static/logo/logo_dragon.png",
    '統一7-ELEVEn獅': f"{settings.API_BASE}/static/logo/logo_lions.png",
    '富邦悍將': f"{settings.API_BASE}/static/logo/logo_fubon.png"
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
                "url": logo_small_url[team.team],
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


def standing_contents(footer: bool = True, share_footer: bool = False):
    standings = game_cache.get_standings()
    contents = [standing_flex(title, teams) for title, teams in standings.items()][::-1]
    if footer:
        for flex in contents:
            flex["footer"] = footer_flex()
    elif share_footer:
        for flex in contents:
            flex["footer"] = share_footer_flex()

    return contents

