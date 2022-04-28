from linebot.models import (
    FlexSendMessage,
)

from mdoel.data_controller import (
    get_game_data
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
    game_infos = get_game_data()
    contents = [game_flex(game) for url, game in game_infos.items()]
    return contents
