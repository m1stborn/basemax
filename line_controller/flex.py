from linebot.models import (
    FlexSendMessage,
)

from mdoel.data_controller import (
    get_games_info,
    get_game_states,
)

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

    # team_away = " 中信兄弟 "
    # team_home = " 中信兄弟 "
    # baseball_field = "新莊棒球場"
    # game_time = "4/28 (三)"
    #
    # current_score = "0:0"
    #
    # team_away_image = image_url[" 中信兄弟 "]
    # team_home_image = image_url[" 中信兄弟 "]

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


def game_state_flex(game_info, game_state):
    team_away = game_info["team_away"]
    team_home = game_info["team_home"]
    pitcher = game_state["pitcher"]
    batter = game_state["batter"]
    inning = game_state["inning"]
    strike = game_state["strike"]
    ball = game_state["ball"]
    out = game_state["out"]

    img_url = "https://raw.githubusercontent.com/m1stborn/CPBL-Linebot/master/assets/100.png"
    try:
        current_score = game_info["current_score"]
    except KeyError:
        current_score = "0:0"
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
                            "text": team_away,
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
                            "text": team_home,
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
                            "text": current_score,
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
                                    "text": strike,
                                    "weight": "bold",
                                    "align": "start",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": ball,
                                    "align": "start",
                                    "gravity": "center",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": out,
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
                                    "text": inning
                                },
                                {
                                    "type": "text",
                                    "text": f"投手: {pitcher} ",
                                    "weight": "bold",
                                    "align": "start",
                                    "gravity": "center"
                                },
                                {
                                    "type": "text",
                                    "text": f"打者: {batter}",
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
    # return {
    #     "type": "bubble",
    #     "header": {
    #         "type": "box",
    #         "layout": "vertical",
    #         "contents": [
    #             {
    #                 "type": "box",
    #                 "layout": "horizontal",
    #                 "contents": [
    #                     {
    #                         "type": "text",
    #                         "text": team_away,
    #                         "align": "end",
    #                         "gravity": "center",
    #                         "weight": "bold",
    #                         "size": "xl"
    #                     },
    #                     {
    #                         "type": "box",
    #                         "layout": "vertical",
    #                         "contents": [
    #                             {
    #                                 "type": "text",
    #                                 "text": "vs",
    #                                 "align": "center",
    #                                 "gravity": "center",
    #                                 "weight": "bold",
    #                                 "size": "xl",
    #                                 "margin": "none"
    #                             }
    #                         ],
    #                         "width": "20%"
    #                     },
    #                     {
    #                         "type": "text",
    #                         "text": team_home,
    #                         "align": "start",
    #                         "gravity": "center",
    #                         "weight": "bold",
    #                         "size": "xl"
    #                     }
    #                 ]
    #             },
    #             {
    #                 "type": "image",
    #                 "url": img_url,
    #                 "margin": "none",
    #                 "size": "4xl",
    #                 "align": "center",
    #                 "offsetTop": "xxl",
    #                 "gravity": "bottom"
    #             },
    #             {
    #                 "type": "box",
    #                 "layout": "horizontal",
    #                 "contents": [
    #                     {
    #                         "type": "text",
    #                         "text": current_score,
    #                         "size": "3xl",
    #                         "align": "center",
    #                         "gravity": "center"
    #                     }
    #                 ]
    #             },
    #             {
    #                 "type": "box",
    #                 "layout": "horizontal",
    #                 "contents": [
    #                     {
    #                         "type": "box",
    #                         "layout": "vertical",
    #                         "contents": [
    #                             {
    #                                 "type": "text",
    #                                 "text": "Strike",
    #                                 "weight": "bold",
    #                                 "align": "start",
    #                                 "gravity": "center"
    #                             },
    #                             {
    #                                 "type": "text",
    #                                 "text": "Ball",
    #                                 "align": "start",
    #                                 "gravity": "center",
    #                                 "weight": "bold"
    #                             },
    #                             {
    #                                 "type": "text",
    #                                 "text": "Out",
    #                                 "weight": "bold",
    #                                 "align": "start",
    #                                 "gravity": "center"
    #                             }
    #                         ],
    #                         "alignItems": "center"
    #                     },
    #                     {
    #                         "type": "box",
    #                         "layout": "vertical",
    #                         "contents": [
    #                             {
    #                                 "type": "text",
    #                                 "text": strike,
    #                                 "weight": "bold",
    #                                 "align": "start",
    #                                 "gravity": "center"
    #                             },
    #                             {
    #                                 "type": "text",
    #                                 "text": ball,
    #                                 "align": "start",
    #                                 "gravity": "center",
    #                                 "weight": "bold"
    #                             },
    #                             {
    #                                 "type": "text",
    #                                 "text": out,
    #                                 "weight": "bold",
    #                                 "align": "start",
    #                                 "gravity": "center"
    #                             }
    #                         ],
    #                         "alignItems": "flex-start",
    #                         "position": "relative",
    #                         "width": "15%",
    #                         "offsetEnd": "xxl"
    #                     },
    #                     {
    #                         "type": "box",
    #                         "layout": "vertical",
    #                         "contents": [
    #                             {
    #                                 "type": "text",
    #                                 "weight": "bold",
    #                                 "align": "end",
    #                                 "gravity": "center",
    #                                 "text": inning
    #                             },
    #                             {
    #                                 "type": "text",
    #                                 "text": f"投手: {pitcher} ",
    #                                 "weight": "bold",
    #                                 "align": "start",
    #                                 "gravity": "center"
    #                             },
    #                             {
    #                                 "type": "text",
    #                                 "text": f"打者: {batter}",
    #                                 "weight": "bold"
    #                             }
    #                         ],
    #                         "alignItems": "flex-start"
    #                     }
    #                 ],
    #                 "alignItems": "flex-end"
    #             }
    #         ]
    #     }
    # }


def today_game():
    game_infos = get_games_info()
    contents = [game_flex(game) for url, game in game_infos.items()]
    return contents


def current_score():
    game_infos = get_games_info()
    # game_states = get_game_states()
    game_states = {
        "/box?year=2022&kindCode=A&gameSno=42": {
        },
        "/box?year=2022&kindCode=A&gameSno=43": {
            'inning': '12局下',
            'pitcher': '江承峰',
            'batter': '林智平',
            'base_wrap': [False, True, False],
            'strike': 2,
            'ball': 2,
            'out': 2
        }
    }
    contents = [game_state_flex(game_infos[url], state)
                for url, state in game_states.items() if state != {}]
    return contents
