import json
import logging
import os
import re
import time
from multiprocessing import Process, Lock
from argparse import Namespace, ArgumentParser
from datetime import date
from typing import Dict
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver

from models import game_cache
from schemas.game import Game, GameState, Play
from utils import error_handler

time.sleep(5)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Can't open multiple driver in docker container,
# will causing the get() function stuck till other driver was closed.

# if os.name == "nt":
#     drivers = [webdriver.Chrome(options=options) for i in range(2)]
#     # driver = webdriver.Chrome(options=options)
# else:
#     drivers = [webdriver.Remote("http://selenium:4444/wd/hub", options=options) for i in range(2)]
#     # driver = webdriver.Remote("http://selenium:4444/wd/hub", options=options)

EMPTY_LINK = 'javascript:;'
BASE_URL = "https://www.cpbl.com.tw"
SCHEDULE_URL = "https://www.cpbl.com.tw/schedule"


def get_driver() -> WebDriver:
    if os.name == "nt":
        driver = webdriver.Chrome(options=options)
    else:
        # options.add_argument('--disable-browser-side-navigation')
        driver = webdriver.Remote("http://selenium:4444/wd/hub", options=options)
    return driver


@error_handler(Exception, logger=logger)
def crawl_today_games_info() -> Dict[str, Game]:
    driver = get_driver()
    driver.get(SCHEDULE_URL)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()

    today = str(date.today().day)

    exclude_day = [25, 26, 27, 28, 29, 30]
    day_soup = soup.findAll('div', class_='date', attrs={'data-date': today})[0 if today not in exclude_day else -1]

    games_soup = day_soup.parent.findAll('div', class_='game')
    team_away = [game.find('div', class_="team away").get_text() for game in games_soup]
    team_away = [re.sub('\\s{2,}', ' ', team) for team in team_away]

    team_home = [game.find('div', class_="team home").get_text() for game in games_soup]
    team_home = [re.sub('\\s{2,}', ' ', team) for team in team_home]

    game_time = [game.find('div', class_="remark").get_text() for game in games_soup]
    game_time = [re.sub('\\s{2,}', ' ', t) for t in game_time]

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
            "game_time": date.today().strftime("%B %d, %Y ") + game_time[i],
        } for i in range(len(game_url_postfix))}

    return {url: Game(**game) for url, game in game_infos.items()}


@error_handler(Exception, logger=logger)
def crawl_score(game_info: Dict) -> Dict:
    driver = get_driver()
    driver.get(game_info['game_live_url'])

    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()

    game_live_soup = soup.find("div", class_="item ScoreBoard")

    team_away = game_live_soup.find("div", class_="team away")
    team_away_score = team_away.find("div", class_="score").get_text() if team_away is not None else ""

    team_home = game_live_soup.find("div", class_="team home")
    team_home_score = team_home.find("div", class_="score").get_text() if team_home is not None else ""

    return {
        **game_info,
        "score": f"{team_away_score}:{team_home_score}"
    }


@error_handler(Exception, logger=logger)
def crawl_game_state(game_url: str) -> Optional[GameState]:
    driver = get_driver()
    driver.get(game_url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()

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
                         out=out, )

    return None


@error_handler(Exception, logger=logger)
def crawl_game_score_plays(game: Game) -> List[Play]:
    driver = get_driver()
    driver.get(game.game_live_url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
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


@error_handler(Exception, logger=logger)
def check_game_start(game_url: str) -> bool:
    driver = get_driver()
    driver.get(game_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    not_start = soup.find("div", class_="game_canceled")

    return not_start is None


@error_handler(Exception, logger=logger)
def check_game_end(game_index_url: str) -> bool:
    driver = get_driver()
    driver.get(game_index_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
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
    logger.info(f"Start tracking: {game.game_url_postfix}")
    scoring_plays = []
    try:
        while True:
            # 1. Check game started
            if not check_game_start(game.game_url):
                continue

            # 2. Get game state
            game_state = crawl_game_state(game.game_url)
            logger.info(f"Game state: {game_state}")
            if game_state is not None and not args.local:
                game_mod.update_one_game_state(game.game_url_postfix, game_state)

            # 3. Get Scoring plays
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
                    game_mod.update_one_game_data(updated_game)

            # 4. Check game end
            if check_game_end(game.game_index_url):
                logger.info(f"Game {game.game_url_postfix} ended.")
                break

            time.sleep(60)

    except KeyboardInterrupt:
        pass

    return

# driver = get_driver()
# def job1():
#     logger.info("start driver 1")
#     for i in range(5):
#         # time.sleep(2)
#         driver.get("https://www.cpbl.com.tw/box?year=2022&kindCode=A&gameSno=53")
#         driver.get("https://www.cpbl.com.tw/box?year=2022&kindCode=A&gameSno=49")
#
#     logger.info("end driver 1")
#
#
# def job2():
#     logger.info("start driver 2")
#     for i in range(5):
#         # time.sleep(2)
#         driver.get("https://www.cpbl.com.tw/box?year=2022&kindCode=A&gameSno=54")
#         driver.get("https://www.cpbl.com.tw/box?year=2022&kindCode=A&gameSno=55")
#
#     logger.info("end driver 2")
#
#
# def test_driver():
#
#     p = mp.Process(target=job2, args=())
#     p.start()
#     job1()
#     p.join()


def main(args):
    # 1. Get Today's Box url
    games = crawl_today_games_info()
    logger.info(f"Init games: {games}")

    if not args.local:
        game_mod.init_data(games)
        game_mod.update_games_data(games)

    # 2. Tracking today's games: only track the game that are not postponed
    games = {k: game for k, game in games.items() if "延賽" not in game.game_time}
    process_list = []
    for i, (k, game) in enumerate(games.items()):
        process_list.append(Process(target=game_tracker, args=(game, args,)))
        process_list[i].start()

    for i, game in enumerate(games):
        process_list[i].join()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--time", action="store_true")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    arg = parse_args()

    if arg.time:
        import time
        t0 = time.time()
        main(arg)
        t1 = time.time()
        total = t1 - t0
        logger.info(f"Total Time: {total} sec")
    else:
        main(arg)
