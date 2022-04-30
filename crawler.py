import json
import re
import time
import multiprocessing as mp
import warnings
import requests
import logging
from typing import List, Dict, Optional
from datetime import date
from argparse import ArgumentParser, Namespace

import schedule
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from mdoel.data_controller import (
    init_data,
    update_games_data,
    update_one_game_data,
    update_one_game_state,
)
from schemas.game import Game, GameState, Play

warnings.filterwarnings("ignore")
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("pyppeteer.launcher").disabled = True
logger = logging.getLogger(__name__)

EMPTY_LINK = 'javascript:;'
BASE_URL = "https://www.cpbl.com.tw"
SCHEDULE_URL = "https://www.cpbl.com.tw/schedule"

session = HTMLSession()


def crawl_today_games_info() -> Dict[str, Game]:
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

    return {url: Game(**game) for url, game in game_infos.items()}


def crawl_score(game_info: Dict) -> Dict:
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


def crawl_game_state(game_url: str) -> Optional[GameState]:
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
        return GameState(inning=inning,
                         pitcher=pitcher,
                         batter=batter,
                         base_wrap=base_wrap,
                         strike=strike,
                         ball=ball,
                         out=out,)

    return None


def crawl_game_score_plays(game: Game) -> List[Play]:
    response = session.get(game.game_live_url, verify=False)
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, "lxml")
    game_live_soup = soup.find("div", class_="InningPlays")
    innings = game_live_soup.findAll("section") if game_live_soup is not None else []

    game_play: List[Play] = []
    for scoring in innings:
        # print(scoring.find("header").next_element.next_element.next_element.replace(' ', ''))
        inning = scoring.find("header").find(text=True, recursive=False).strip()
        plays = scoring.findAll("div", class_="item play")
        for play in plays:
            play_desc = play.find("div", class_="desc").get_text()
            play_desc_clean = re.sub('\\s{2,}', ' ', play_desc)
            score = play.find("div", class_="vs_box").get_text()

            score = score.replace("富邦悍將", game.team_home)
            score = score.replace("Rakuten Monkeys", game.team_away)

            game_play.append(Play(inning=inning,
                                  play=play_desc_clean,
                                  score=score))

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


def stream_scoring_play(game: Game, plays: List[Play]):
    url = "https://cpbl-linebot.herokuapp.com/game/scoring_play"
    payload = {
        "game_url_postfix": game.game_url_postfix,
        "scoring_play": json.loads(json.dumps(plays, default=vars))
    }
    response = requests.post(url, json=payload)

    if response.status_code == 400:
        logger.error(f"Status code 400: payload = {payload}")


def game_tracker(game: Game, args):
    try:
        while True:
            # Check game started
            if check_game_start(game.game_url):
                scoring_plays = []
                while True:
                    game_state = crawl_game_state(game.game_url)
                    if game_state is not None:
                        update_one_game_state(game.game_url_postfix, game_state)

                    tmp_scoring_plays = crawl_game_score_plays(game)
                    if len(tmp_scoring_plays) > len(scoring_plays):
                        new_scoring_plays = tmp_scoring_plays[len(scoring_plays):]
                        logger.info(f"Game: {game.game_url}, New scoring play = {new_scoring_plays}")

                        scoring_plays = tmp_scoring_plays
                        current_score = scoring_plays[-1].score.split(" ")

                        updated_game = game
                        updated_game.current_score = "".join(current_score[3:6])
                        updated_game.scoring_play = scoring_plays

                        if not args.local:
                            stream_scoring_play(game, new_scoring_plays)
                            update_one_game_data(updated_game)

                    if check_game_end(game.game_index_url):
                        break
                    time.sleep(60)
            if check_game_end(game.game_index_url):
                break
    except KeyboardInterrupt:
        pass

    return


def main(args):
    logger.info("Start tracking")

    # 1. Get Today's Box url
    games = crawl_today_games_info()

    logger.info(f"Init games: {games}")

    if not args.local:
        init_data(games)
        update_games_data(games)

    # 2. Get box live
    process_list = []
    for i, (k, game) in enumerate(games.items()):
        process_list.append(mp.Process(target=game_tracker, args=(game, args,)))
        process_list[i].start()

    for i, game in enumerate(games):
        process_list[i].join()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--local", action="store_true")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    arg = parse_args()
    main(arg)
    # schedule.every().day.at("00:00").do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
