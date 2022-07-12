from typing import List, Optional
from pydantic import BaseModel

from schemas.player import Batter, Pitcher


class Play(BaseModel):
    inning: str
    play: str
    score: str


class Game(BaseModel):
    game_url_postfix: str
    team_home: str
    team_away: str
    game_url: str
    game_live_url: str
    game_index_url: str
    baseball_field: str
    game_time: str
    current_score: Optional[str]
    scoring_play: Optional[List[Play]]


class GameState(BaseModel):
    inning: str
    pitcher: str
    batter: str
    base_wrap: List[bool]
    strike: int
    ball: int
    out: int
    scores: List[List] = None
    scores_fixed: List[List] = None


class GameBox(BaseModel):
    game_url_postfix: str = ""
    game_title: str = ""
    game_time_int: str = ""
    away_bat_box: Optional[List[Batter]]
    away_pitch_box: Optional[List[Pitcher]]
    home_bat_box: Optional[List[Batter]]
    home_pitch_box: Optional[List[Pitcher]]


# class Games(BaseModel):
#     def __getitem__(self, index):
#         Ga


if __name__ == "__main__":
    box = GameBox()
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
    game = Game(**test_game_info)
    print(game.scoring_play[0].score)
