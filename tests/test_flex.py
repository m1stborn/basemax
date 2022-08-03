import json

from line.game_flex import match_flex
from schemas.game import Game

mock_game = Game(game_url_postfix='/box?year=2022&kindCode=A&gameSno=178',
                 team_home='富邦悍將',
                 team_away='中信兄弟',
                 game_url='https://www.cpbl.com.tw/box?year=2022&kindCode=A&gameSno=178',
                 game_live_url='https://www.cpbl.com.tw/box/live?year=2022&kindCode=A&gameSno=178',
                 game_index_url='https://www.cpbl.com.tw/box/index?year=2022&kindCode=A&gameSno=178',
                 baseball_field='新莊',
                 game_time='August 03, 2022  18:35',
                 current_score=None,
                 scoring_play=None)


# def test_match_flex() -> None:
#     mock_flex = match_flex(mock_game)
#     with open("tests/mock_match_flex.json", encoding="utf-8") as file:
#         flex = json.load(file)
#
#     assert mock_flex == flex
