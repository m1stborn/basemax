import re
from typing import Union, List, Optional
from pydantic import BaseModel


class Batter(BaseModel):
    num: str
    name: str
    pos: str
    at_bat: str
    run: str
    hit: str
    rbi: str
    bb: str
    so: str
    avg: str

    @classmethod
    def from_list(cls, row: List[str]):
        # Hard coding the scraped list
        sub = re.sub(r"[()]", "", row[0])
        names = re.split(r'(\d*)([\u4e00-\u9fff．]+)([\d*a-zA-z(),\s]+)', sub)[1:-1]
        if len(names) == 0:  # handle total row
            names = [' ', 'Total', ' ']
        values = names + row[1:5] + [row[9], row[12], row[-1].replace("0", "").replace("empty", " ")]

        keys = cls.__fields__.keys()
        team_dict = dict(zip(keys, values))

        return cls(**team_dict)


class Pitcher(BaseModel):
    num: str
    name: str
    pos: Union[str, None]
    ip: str
    pc: str
    hit: str
    run: str
    er: str
    bb: str
    k: str
    era: str
    whip: str

    @classmethod
    def from_list(cls, row: List[str]):
        # Hard coding the scraped list
        sub = re.sub(r"[(),]", "", row[0])
        names = re.split(r'(\d*)([\u4e00-\u9fff．]+)([\d*a-zA-z(),\s]+)?', sub)[1:-1]
        if len(names) == 0:  # handle total row
            names = [' ', 'Total', ' ']
        ip = re.split(r"(\d)(\d)?(\d)(/)", row[1])
        ip = f"{ip[0]}" if len(ip) == 1 else f"{ip[1]}{ip[2] if ip[2] else ''}.{ip[3]}"

        # Easy to hande 1 digit
        # ips = row[1].split("/")
        # ip = f"{ips[0]}" + f".{row[1][-2]}" if len(ips) > 1 else ""

        values = names + [ip] + [row[3], row[5], row[-5], row[-4], row[7], row[10]] + row[-2:]
        keys = cls.__fields__.keys()
        team_dict = dict(zip(keys, values))
        return cls(**team_dict)
