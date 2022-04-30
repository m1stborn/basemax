import json
import time
import requests
import pprint
from argparse import ArgumentParser

from mdoel.data_controller import (
    update_one_game_state,
    update_one_game_data,
    update_broadcast_list,
    update_games_data,
    get_game_state,
    get_games_info,
    get_game_states,
)

test_game_url = "/box?year=2022&kindCode=A&gameSno=44"

test_game_state = {
    'inning': '12局下',
    'pitcher': '江承峰',
    'batter': '林智平',
    'base_wrap': [False, True, True],
    'strike': 2,
    'ball': 2,
    'out': 0
}

test_game_info = {
        "team_home": " 味全龍 ",
        "team_away": " 統一7-ELEVEn獅 ",
        "game_url_postfix": "/box?year=2022&kindCode=A&gameSno=38",
        "game_url": "https://www.cpbl.com.tw/box?year=2022&kindCode=A&gameSno=38",
        "game_live_url": "https://www.cpbl.com.tw/box/live?year=2022&kindCode=A&gameSno=38",
        "game_index_url": "https://www.cpbl.com.tw/box/index?year=2022&kindCode=A&gameSno=38",
        "baseball_field": " 天母 ",
        "game_time": "April 28, 2022",
        "scoring_play": [
            {
                "inning": "3 下",
                "play": " 第3棒 RF 陳品捷： 擊出右外野滾地球，一壘安打 。1分打點。 三壘跑者郭天信回本壘得分。 一壘跑者林智勝 上二壘。 ",
                "score": " 統一7-ELEVEn獅  0 : 1  味全龍 "
            },
            {
                "inning": "4 下",
                "play": " 第8棒 3B 劉基鴻： 擊出中外野高飛球，二壘安打 。1分打點。 三壘跑者拿莫．伊漾回本壘得分。 ",
                "score": " 統一7-ELEVEn獅  0 : 2  味全龍 "
            },
            {
                "inning": "4 下",
                "play": " 第9棒 SS 張政禹： 擊出左外野高飛球，二壘安打 。1分打點。 二壘跑者劉基鴻回本壘得分。 ",
                "score": " 統一7-ELEVEn獅  0 : 3  味全龍 "
            },
            {
                "inning": "7 下",
                "play": " 第6棒 1B 拿莫．伊漾： 擊出左外野高飛球，一壘安打 。1分打點。 二壘跑者吉力吉撈．鞏冠回本壘得分。 一壘跑者李凱威 上二壘。 二壘跑者李凱威 因左外野手 失誤上三壘。 一壘跑者拿莫．伊漾 因左外野手 失誤上二壘。 ",
                "score": " 統一7-ELEVEn獅  0 : 4  味全龍 "
            },
            {
                "inning": "7 下",
                "play": " 第7棒 LF 張祐銘： 擊出左外野高飛球， 打者出局-犧牲飛球出局。1分打點。 1人出局。 三壘跑者李凱威回本壘得分。 二壘跑者拿莫．伊漾 因左外野手 傳捕手失誤上三壘。 ",
                "score": " 統一7-ELEVEn獅  0 : 5  味全龍 "
            },
            {
                "inning": "7 下",
                "play": " 第8棒 3B 劉基鴻： 擊出右外野高飛球，一壘安打 。1分打點。 三壘跑者拿莫．伊漾回本壘得分。 ",
                "score": " 統一7-ELEVEn獅  0 : 6  味全龍 "
            },
            {
                "inning": "8 上",
                "play": " 第1棒 CF 陳傑憲： 擊出左外野高飛球， 打者出局-犧牲飛球出局。1分打點。 2人出局。 三壘跑者柯育民回本壘得分。 ",
                "score": " 統一7-ELEVEn獅  1 : 6  味全龍 "
            },
            {
                "inning": "8 下",
                "play": " 第5棒 2B 李凱威： 擊出中外野高飛球，二壘安打 。1分打點。 二壘跑者邱辰回本壘得分。 一壘跑者吉力吉撈．鞏冠 上三壘。 ",
                "score": " 統一7-ELEVEn獅  1 : 7  味全龍 "
            }
        ],
        "current_score": "1:7"
    }

if __name__ == "__main__":
    # Show Game State
    # update_one_game_state(test_game_url, test_game_state)

    # Show live broadcast
    # update_one_game_data(test_game_info)

    # broadcast_feed = test_game_info["scoring_play"][-3:]
    # for feed in broadcast_feed:
    #     url = "https://cpbl-linebot.herokuapp.com/game/scoring_play"
    #     payload = {
    #         "game_url_postfix": test_game_url,
    #         "scoring_play": [feed]
    #     }
    #     response = requests.post(url, json=payload)
    #     time.sleep(10)

    info_before = get_games_info()
    update_games_data(info_before)
    info_after = get_games_info()

    assert info_after == info_before

    update_one_game_data(get_games_info()["/box?year=2022&kindCode=A&gameSno=44"])
    info_after = get_games_info()
    assert info_after == info_before

    game_state_before = get_game_states()
    state = game_state_before["/box?year=2022&kindCode=A&gameSno=44"]
    update_one_game_state(test_game_url, state)
    game_state_after = get_game_states()
    assert game_state_after == game_state_before
