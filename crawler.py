import re
import json
import time
import multiprocessing as mp
import warnings
import requests
from pathlib import Path
from typing import List, Dict
from datetime import date
from argparse import ArgumentParser, Namespace

from bs4 import BeautifulSoup
from requests_html import HTMLSession

from mdoel.data_controller import (
    init_data,
    update_games_data,
    update_one_game_data,
    update_one_game_state,
)

warnings.filterwarnings("ignore")

EMPTY_LINK = 'javascript:;'

BASE_URL = "https://www.cpbl.com.tw"
SCHEDULE_URL = "https://www.cpbl.com.tw/schedule"

session = HTMLSession()


def get_today_games_info() -> Dict:
    response = session.get(SCHEDULE_URL, verify=False)
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, "lxml")

    today = str(date.today().day)

    day_soup = soup.findAll('div', class_='date', attrs={'data-date': today})[-1]
    games_soup = day_soup.parent.findAll('div', class_='game')

    team_away = [game.find('div', class_="team away").get_text() for game in games_soup]
    team_away = [re.sub('\\s{2,}', ' ', team) for team in team_away]

    team_home = [game.find('div', class_="team home").get_text() for game in games_soup]
    team_home = [re.sub('\\s{2,}', ' ', team) for team in team_home]

    place = [game.find('div', class_="place").get_text() for game in games_soup]

    result = day_soup.parent.findAll('a') if day_soup is not None else []
    game_url_postfix = [game['href'] for game in result if game['href'] != EMPTY_LINK]

    game_infos = {
        game_url_postfix[i]: {
            "team_home": team_home[i],
            "team_away": team_away[i],
            "game_url_postfix": game_url_postfix[i],
            "game_url": BASE_URL + game_url_postfix[i],
            "game_live_url": BASE_URL + game_url_postfix[i].replace('/box', '/box/live'),
            "game_index_url": BASE_URL + game_url_postfix[i].replace('/box', '/box/index'),
            "baseball_field": place[i],
            "game_time": date.today().strftime("%B %d, %Y"),
        } for i in range(len(game_url_postfix))}

    return game_infos


def get_score(game_info: Dict) -> Dict:
    response = session.get(game_info['game_live_url'], verify=False)
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, "lxml")

    game_live_soup = soup.find("div", class_="item ScoreBoard")

    team_away = game_live_soup.find("div", class_="team away")
    team_away_score = team_away.find("div", class_="score").get_text() if team_away is not None else ""

    team_home = game_live_soup.find("div", class_="team home")
    team_home_score = team_home.find("div", class_="score").get_text() if team_home is not None else ""

    return {
        **game_info,
        "score": f"{team_away_score}:{team_home_score}"
    }


def get_game_state(game_url: str) -> Dict or None:
    response = session.get(game_url, verify=False)
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, "lxml")

    game_state_soup = soup.find("div", class_="item GameMatchup")
    if game_state_soup is not None:
        # print(game_state_soup.prettify())
        inning = game_state_soup.find("div", class_="title").get_text()

        pitcher = game_state_soup.find("div", class_="picther")
        pitcher = pitcher.find("div", class_="player").get_text()

        batter = game_state_soup.find("div", class_="batter")
        batter = batter.find("div", class_="player").get_text()

        base_wrap = game_state_soup.find("div", class_="bases_wrap").findAll("span")
        base_wrap = [len(base["class"]) == 3 for base in base_wrap]

        sbo = game_state_soup.find("div", class_="sbo")
        strike = sbo.find("div", class_="strike").findAll("span")
        strike = sum([len(s["class"]) == 2 for s in strike])

        ball = sbo.find("div", class_="ball").findAll("span")
        ball = sum([len(s["class"]) == 2 for s in ball])

        out = sbo.find("div", class_="out").findAll("span")
        out = sum([len(s["class"]) == 2 for s in out])

        return {
            "inning": inning,
            "pitcher": pitcher,
            "batter": batter,
            "base_wrap": base_wrap,
            "strike": strike,
            "ball": ball,
            "out": out,
        }
    return None


def get_game_score_plays(game_info: Dict) -> List[Dict]:
    response = session.get(game_info['game_live_url'], verify=False)
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, "lxml")
    game_live_soup = soup.find("div", class_="InningPlays")
    innings = game_live_soup.findAll("section") if game_live_soup is not None else []

    game_play: List[Dict] = []
    for scoring in innings:
        # print(scoring.find("header").next_element.next_element.next_element.replace(' ', ''))
        inning = scoring.find("header").find(text=True, recursive=False).strip()
        plays = scoring.findAll("div", class_="item play")
        for play in plays:
            play_desc = play.find("div", class_="desc").get_text()
            play_desc_clean = re.sub('\\s{2,}', ' ', play_desc)
            score = play.find("div", class_="vs_box").get_text()

            score = score.replace("富邦悍將", game_info["team_home"])
            score = score.replace("Rakuten Monkeys", game_info["team_away"])

            game_play.append({
                "inning": inning,
                "play": play_desc_clean,
                "score": score,
            })

    return game_play


def check_game_start(game_url: str) -> bool:
    response = session.get(game_url, verify=False)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, "lxml")

    not_start = soup.find("div", class_="game_canceled")

    return not_start is None


def check_game_end(game_index_url: str) -> bool:
    response = session.get(game_index_url, verify=False)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, "lxml")

    # game_brief = soup.find("div", class_="GameNote")
    game_brief = soup.find("div", class_="editable_content")

    return game_brief is not None


def game_tracker(game_info: Dict, args):
    try:
        while True:
            # Check game started
            if check_game_start(game_info['game_url']):
                scoring_plays = []
                while True:
                    game_state = get_game_state(game_info['game_url'])
                    if game_state is not None:
                        update_one_game_state(game_info['game_url_postfix'], game_state)

                    tmp_scoring_plays = get_game_score_plays(game_info)
                    if len(tmp_scoring_plays) > len(scoring_plays):
                        print(tmp_scoring_plays[len(scoring_plays):])

                        # if not args.local:
                        #     url = "https://cpbl-linebot.herokuapp.com/game/scoring_play"
                        #     payload = {
                        #         "game_url_postfix": game_info['game_url_postfix'],
                        #         "scoring_play": tmp_scoring_plays[len(scoring_plays):]
                        #     }
                        #     response = requests.post(url, json=payload)

                        scoring_plays = tmp_scoring_plays
                        current_score = scoring_plays[-1]["score"].split(" ")

                        if not args.local:
                            update_one_game_data({
                                **game_info,
                                "scoring_play": scoring_plays,
                                "current_score": "".join(current_score[3:6])
                            })

                    if check_game_end(game_info['game_index_url']):
                        break
                    time.sleep(60)
            if check_game_end(game_info['game_index_url']):
                break
    except KeyboardInterrupt:
        pass

    return


def main(args):
    print("Start Tracking")
    # 1. Get Today's Box url
    game_infos = get_today_games_info()
    print(game_infos)

    if not args.local:
        init_data(game_infos)
        update_games_data(game_infos)

    # 2. Get box live
    process_list = []
    for i, (k, game_info) in enumerate(game_infos.items()):
        process_list.append(mp.Process(target=game_tracker, args=(game_info, args,)))
        process_list[i].start()

    for i, game_info in enumerate(game_infos):
        process_list[i].join()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--local", action="store_true")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    arg = parse_args()
    main(arg)
    # schedule.every().day.at("02:51").do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
