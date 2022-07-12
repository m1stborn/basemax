from config import Setting
from line.footer_flex import footer_flex
from models.game_cache import (
    get_games_info,
    get_game_states,
)
from schemas.game import Game, GameState

settings = Setting()

logo_large_url = {
    '樂天桃猿': f'{settings.API_BASE}/static/logo/logo_monkeys_large.png',
    '中信兄弟': f'{settings.API_BASE}/static/logo/logo_brothers_large.png',
    '味全龍': f'{settings.API_BASE}/static/logo/logo_dragon_large.png',
    '統一7-ELEVEn獅': f'{settings.API_BASE}/static/logo/logo_lions_large.png',
    '富邦悍將': f'{settings.API_BASE}/static/logo/logo_fubon_large.png'
}

base_wrap_image = {
    "000": f'{settings.API_BASE}/static/base/000.png',
    "001": f'{settings.API_BASE}/static/base/001.png',
    "010": f'{settings.API_BASE}/static/base/010.png',
    "011": f'{settings.API_BASE}/static/base/011.png',
    "100": f'{settings.API_BASE}/static/base/100.png',
    "110": f'{settings.API_BASE}/static/base/110.png',
    "111": f'{settings.API_BASE}/static/base/111.png',
    "101": f'{settings.API_BASE}/static/base/101.png'
}

team_name_map = {
    '樂天桃猿': '樂天桃猿',
    '中信兄弟': '中信兄弟',
    '味全龍': '味全龍',
    '統一7-ELEVEn獅': '統一獅',
    '富邦悍將': '富邦悍將'
}

short_team = {
    '樂天桃猿': '樂天',
    '中信兄弟': '中信',
    '味全龍': '味全',
    '統一7-ELEVEn獅': '統一',
    '富邦悍將': '富邦'
}


def scoreboard_header_cell(inning: int):
    return {
        "type": "text",
        "text": str(inning),
        "flex": 2,
        "color": "#9FA8DA",
        "size": "xxs",
        "weight": "bold",
        "align": "center",
        "gravity": "center"
    }


def scoreboard_row_cell(text: str):
    return {
        "type": "text",
        "text": text,
        "flex": 2,
        "size": "xxs",
        "align": "center",
        "gravity": "center"
    }


def scoreboard_flex(game: Game, game_state: GameState):
    wrap = "".join([str(int(b)) for b in game_state.base_wrap])
    img_url = base_wrap_image[wrap]
    current_scores = game.current_score if game.current_score is not None else "0:0"

    inning_len = len(game_state.scores[0])
    headers = [scoreboard_header_cell(i) for i in range(inning_len)]

    game_state.scores[0] += ['-' for i in range(9-len(game_state.scores[0]))]
    game_state.scores[1] += ['-' for i in range(9-len(game_state.scores[1]))]
    away_team_row = [scoreboard_row_cell(text) for text in game_state.scores[0]]
    home_team_row = [scoreboard_row_cell(text) for text in game_state.scores[1]]

    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": team_name_map[game.team_away],
                            "align": "end",
                            "gravity": "center",
                            "weight": "bold",
                            "size": "xl",
                            "flex": 5
                        },
                        {
                            "type": "text",
                            "text": current_scores.replace(":", " : "),
                            "align": "center",
                            "gravity": "center",
                            "weight": "bold",
                            "size": "xl",
                            "margin": "none",
                            "flex": 4
                        },
                        {
                            "type": "text",
                            "text": team_name_map[game.team_home],
                            "align": "start",
                            "gravity": "center",
                            "weight": "bold",
                            "size": "xl",
                            "flex": 5
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "separator",
                            "color": "#9FA8DA"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                {
                                    "type": "text",
                                    "text": "Team",
                                    "flex": 5,
                                    "color": "#9FA8DA",
                                    "size": "sm",
                                    "align": "center",
                                    "weight": "bold"
                                },
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                *headers,
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                {
                                    "type": "text",
                                    "text": "R",
                                    "flex": 2,
                                    "color": "#9FA8DA",
                                    "size": "xxs",
                                    "weight": "bold",
                                    "align": "center",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "H",
                                    "flex": 2,
                                    "color": "#9FA8DA",
                                    "size": "xxs",
                                    "weight": "bold",
                                    "align": "center",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "E",
                                    "flex": 2,
                                    "color": "#9FA8DA",
                                    "size": "xxs",
                                    "weight": "bold",
                                    "align": "center",
                                    "gravity": "center"
                                },
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "color": "#9FA8DA"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                {
                                    "type": "text",
                                    "text": short_team[game.team_away],
                                    "flex": 5,
                                    "size": "sm",
                                    "align": "center"
                                },
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                *away_team_row,
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                {
                                    "type": "text",
                                    "text": game_state.scores_fixed[0][0],
                                    "flex": 2,
                                    "size": "xxs",
                                    "align": "center",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": game_state.scores_fixed[0][1],
                                    "flex": 2,
                                    "size": "xxs",
                                    "align": "center",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": game_state.scores_fixed[0][2],
                                    "flex": 2,
                                    "size": "xxs",
                                    "align": "center",
                                    "gravity": "center"
                                },
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                {
                                    "type": "text",
                                    "text": short_team[game.team_home],
                                    "flex": 5,
                                    "size": "sm",
                                    "align": "center"
                                },
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                *home_team_row,
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                {
                                    "type": "text",
                                    "text": game_state.scores_fixed[0][0],
                                    "flex": 2,
                                    "size": "xxs",
                                    "align": "center",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": game_state.scores_fixed[0][1],
                                    "flex": 2,
                                    "size": "xxs",
                                    "align": "center",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": game_state.scores_fixed[0][2],
                                    "flex": 2,
                                    "size": "xxs",
                                    "align": "center",
                                    "gravity": "center"
                                },
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "color": "#9FA8DA"
                        }
                    ],
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "separator",
                                            "color": "#9FA8DA"
                                        },
                                        {
                                            "type": "text",
                                            "text": "Strike",
                                            "flex": 4,
                                            "color": "#9FA8DA",
                                            "weight": "bold",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(game_state.strike),
                                            "flex": 1,
                                            "size": "sm"
                                        },
                                        {
                                            "type": "separator",
                                            "color": "#9FA8DA"
                                        },
                                        {
                                            "type": "text",
                                            "text": game_state.inning,
                                            "flex": 7,
                                            "size": "sm",
                                            "align": "center"
                                        },
                                        {
                                            "type": "separator",
                                            "color": "#9FA8DA"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "separator",
                                            "color": "#9FA8DA"
                                        },
                                        {
                                            "type": "text",
                                            "text": "Ball",
                                            "flex": 4,
                                            "color": "#9FA8DA",
                                            "weight": "bold",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(game_state.ball),
                                            "flex": 1,
                                            "size": "sm"
                                        },
                                        {
                                            "type": "separator",
                                            "color": "#9FA8DA"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"投手: {game_state.pitcher}",
                                            "flex": 7,
                                            "size": "sm",
                                            "align": "center"
                                        },
                                        {
                                            "type": "separator",
                                            "color": "#9FA8DA"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "separator",
                                            "color": "#9FA8DA"
                                        },
                                        {
                                            "type": "text",
                                            "text": "Out",
                                            "flex": 4,
                                            "color": "#9FA8DA",
                                            "weight": "bold",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(game_state.out),
                                            "flex": 1,
                                            "size": "sm"
                                        },
                                        {
                                            "type": "separator",
                                            "color": "#9FA8DA"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"打者: {game_state.batter}",
                                            "flex": 7,
                                            "size": "sm",
                                            "align": "center"
                                        },
                                        {
                                            "type": "separator",
                                            "color": "#9FA8DA"
                                        }
                                    ]
                                },
                                {
                                    "type": "separator",
                                    "color": "#9FA8DA"
                                }
                            ],
                            "flex": 6,
                            "justifyContent": "center"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "image",
                                    "url": img_url,
                                    "size": "4xl",
                                    "align": "center",
                                    "gravity": "center"
                                }
                            ],
                            "flex": 4,
                            "margin": "sm",
                            "justifyContent": "center"
                        }
                    ]
                }
            ]
        }
    }


def scoreboard_innings_contents(footer: bool = True):
    game = get_games_info()
    game_states = get_game_states()

    contents = [scoreboard_flex(game[url], state)
                for url, state in game_states.items() if state != {}]

    # TODO: refactor footer
    if footer:
        for flex in contents:
            flex["footer"] = footer_flex(post_fix="/score")

    return contents
