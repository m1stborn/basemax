from typing import Union, List
from pydantic import BaseModel


class Team(BaseModel):
    ranking: str
    team: str
    win: str
    tie: str
    lose: str
    win_rate: str
    game_behind: str

    @classmethod
    def from_list(cls, row: List[str]):
        # Hard coding the scraped list
        values = [row[0][0], row[0][1:]] + row[2].split("-") + [row[3].replace("0.", ".")] + [row[4]]
        keys = cls.__fields__.keys()
        team_dict = dict(zip(keys, values))

        return cls(**team_dict)


class Standing(BaseModel):
    teams: List[Team]
