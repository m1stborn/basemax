from linebot.models import (
    FlexSendMessage,
)

from line.footer_flex import footer_flex
from models.game_cache import (
    get_games_info,
    get_game_states,
)
from schemas.game import Game, GameState

logo_large_url = {
    "中信兄弟": "https://www.dropbox.com/s/ey3sjbds59umt9p/logo_brothers_large.png?dl=1",
    "味全龍": "https://www.dropbox.com/s/rqgyx6zaaf4sj8h/logo_dragon_large.png?dl=1",
    "富邦悍將": "https://www.dropbox.com/s/94aq394s7w3b5wu/logo_fubon_large.png?dl=1",
    "統一7-ELEVEn獅": "https://www.dropbox.com/s/9ckrf50o8m3hj71/logo_lions_large.png?dl=1",
    "樂天桃猿": "https://www.dropbox.com/s/e0qbbbdb1ul5dm2/logo_monkeys_large.png?dl=1"
}

base_wrap_image = {
    "000": "https://www.dropbox.com/s/h4o0osgrz7xh82b/000.png?dl=1",
    "001": "https://www.dropbox.com/s/vvadsdj9mzlidv4/001.png?dl=1",
    "010": "https://www.dropbox.com/s/ff5590ug7612uzk/010.png?dl=1",
    "011": "https://www.dropbox.com/s/18vwj9g4l9tg1z5/011.png?dl=1",
    "100": "https://www.dropbox.com/s/3k5qhysl2po8l7h/100.png?dl=1",
    "110": "https://www.dropbox.com/s/465tmx3uhgp3qz1/110.png?dl=1",
    "111": "https://www.dropbox.com/s/8asj2xtmyjowp7m/111.png?dl=1"
}


def flex_message_wrapper(alt: str, contents: list or dict, **kwargs):
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


def match_flex(game: Game):
    current_scores = game.current_score if game.current_score is not None else "0:0"
    team_away_image = logo_large_url[game.team_away]
    team_home_image = logo_large_url[game.team_home]

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
                            "text": game.team_away,
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
                            "text": game.team_home,
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
                    "text": current_scores,
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
                    "text": game.baseball_field,
                    "weight": "bold",
                    "align": "center",
                    "gravity": "center"
                },
                {
                    "type": "text",
                    "text": game.game_time,
                    "weight": "bold",
                    "align": "center",
                    "gravity": "center"
                }
            ]
        }
    }


def game_state_flex(game: Game, game_state: GameState):
    wrap = "".join([str(int(b)) for b in game_state.base_wrap])
    img_url = base_wrap_image[wrap]
    current_scores = game.current_score if game.current_score is not None else "0:0"
    print("game_state_flex", current_scores)
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
                            "text": game.team_away,
                            "align": "end",
                            "gravity": "center",
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "vs",
                                    "align": "center",
                                    "gravity": "center",
                                    "weight": "bold",
                                    "size": "xl",
                                    "margin": "none"
                                }
                            ],
                            "width": "20%"
                        },
                        {
                            "type": "text",
                            "text": game.team_home,
                            "align": "start",
                            "gravity": "center",
                            "weight": "bold",
                            "size": "xl"
                        }
                    ]
                },
                {
                    "type": "image",
                    "url": img_url,
                    "margin": "none",
                    "size": "4xl",
                    "align": "center",
                    "offsetTop": "xxl",
                    "gravity": "bottom"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": current_scores,
                            "size": "3xl",
                            "align": "center",
                            "gravity": "center"
                        }
                    ]
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
                                    "type": "text",
                                    "text": "Strike",
                                    "weight": "bold",
                                    "align": "start",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "Ball",
                                    "align": "start",
                                    "gravity": "center",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "Out",
                                    "weight": "bold",
                                    "align": "start",
                                    "gravity": "center"
                                }
                            ],
                            "alignItems": "center"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": str(game_state.strike),
                                    "weight": "bold",
                                    "align": "start",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": str(game_state.ball),
                                    "align": "start",
                                    "gravity": "center",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": str(game_state.out),
                                    "weight": "bold",
                                    "align": "start",
                                    "gravity": "center"
                                }
                            ],
                            "alignItems": "flex-start",
                            "position": "relative",
                            "width": "15%",
                            "offsetEnd": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "weight": "bold",
                                    "align": "end",
                                    "gravity": "center",
                                    "text": game_state.inning
                                },
                                {
                                    "type": "text",
                                    "text": f"投手: {game_state.pitcher} ",
                                    "weight": "bold",
                                    "align": "start",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": f"打者: {game_state.batter}",
                                    "weight": "bold"
                                }
                            ],
                            "alignItems": "flex-start"
                        }
                    ],
                    "alignItems": "flex-end"
                }
            ]
        }
    }


def match_contents(footer: bool = True):
    games = get_games_info()
    contents = [match_flex(game) for url, game in games.items()]

    if footer:
        for flex in contents:
            flex["footer"] = footer_flex(post_fix="/match")

    return contents


def scoreboard_contents(footer: bool = True):
    game = get_games_info()
    game_states = get_game_states()

    contents = [game_state_flex(game[url], state)
                for url, state in game_states.items() if state != {}]
    if footer:
        for flex in contents:
            flex["footer"] = footer_flex(post_fix="/score")

    return contents
