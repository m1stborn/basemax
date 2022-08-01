import json
import logging
import os
import re
import time
import uuid
from argparse import Namespace, ArgumentParser
from datetime import date, datetime, timedelta
from multiprocessing import Process, Lock
from random import randint
from typing import Dict, Union
from typing import List, Optional

import jwt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from config import Setting, CPBLSetting
from line.verify import AutoVerify
from models import game_cache
from schemas.game import Game, GameState, Play, GameBox
from schemas.player import Batter, Pitcher
from schemas.standing import Team
from utils import error_handler


settings = Setting()
cpbl = CPBLSetting()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

browser_lock = Lock()

if os.name == "nt":
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)

    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--log-level=3")
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # browser = webdriver.Chrome(options=options)

else:
    # In container env, need to wait til Remote WebDriver is opened.
    time.sleep(15)
    # options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")
    # browser = webdriver.Remote("http://selenium:4444/wd/hub", options=options,
    #                            desired_capabilities=DesiredCapabilities.FIREFOX)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Remote("http://selenium:4444/wd/hub", options=options)


def get_page(url: str, wait: int = 0) -> str:
    with browser_lock:
        browser.get(url)
        time.sleep(wait)
        source = browser.page_source
        # TODO: actually needed?
        if len(browser.window_handles) >= 2:
            print(browser.window_handles, len(browser.window_handles))
            browser.close()
    return source


# TODO: custom date include month
@error_handler(Exception, logger=logger)
def crawl_today_games_info(wait: int = 0.5, days: int = None) -> Dict[str, Game]:
    page = get_page(cpbl.CPBL_SCHEDULE_URL, wait)
    soup = BeautifulSoup(page, "html.parser")

    today = int(date.today().day) if days is None else days

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
    game_url_postfix = [game['href'] for game in result if game['href'] != cpbl.EMPTY_LINK]

    game_infos = {
        game_url_postfix[i]: {
            "team_home": team_home[i].strip(),
            "team_away": team_away[i].strip(),
            "game_url_postfix": game_url_postfix[i],
            "game_url": cpbl.CPBL_BASE_URl + game_url_postfix[i],
            "game_live_url": cpbl.CPBL_BASE_URl + game_url_postfix[i].replace('/box', '/box/live'),
            "game_index_url": cpbl.CPBL_BASE_URl + game_url_postfix[i].replace('/box', '/box/index'),
            "baseball_field": place[i].strip(),
            "game_time": date.today().strftime("%B %d, %Y ") + game_time[i],
        } for i in range(len(game_url_postfix))}

    return {url: Game(**game) for url, game in game_infos.items()}


@error_handler(Exception, logger=logger)
def crawl_game_scoreboard(game_url: str, wait: int = 0.5) -> (List, List):
    page = get_page(game_url, wait)
    soup = BeautifulSoup(page, "html.parser")

    scoreboard = soup.find("div", class_="linescore scrollable")
    scoreboard_fixed = soup.find("div", class_="linescore fixed")

    score_fixed = []
    scores = []

    if scoreboard_fixed is not None:
        rows = scoreboard_fixed.find_all('tr')
        for row in rows[1:]:  # Skip first header row
            cols = row.find_all('td')
            cols = [ele.text.strip().replace("\n\n", "") for ele in cols]
            score_fixed.append([ele for ele in cols if ele])

    if scoreboard is not None:
        rows = scoreboard.find_all('tr')
        for row in rows[1:]:  # Skip first header row
            cols = row.find_all('td')
            cols = [ele.text.strip().replace("\n\n", "") for ele in cols]
            scores.append([ele for ele in cols if ele])

    return scores, score_fixed


@error_handler(Exception, logger=logger)
def crawl_game_state(game_url: str, wait: int = 0.5) -> Optional[GameState]:
    page = get_page(game_url, wait)
    soup = BeautifulSoup(page, "html.parser")

    game_state_soup = soup.find("div", class_="item GameMatchup")
    if game_state_soup is not None:
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

        # scoreboard
        scoreboard = soup.find("div", class_="linescore scrollable")
        scoreboard_fixed = soup.find("div", class_="linescore fixed")

        scores_fixed = []
        scores = []

        if scoreboard_fixed is not None:
            rows = scoreboard_fixed.find_all('tr')
            for row in rows[1:]:  # Skip first header row
                cols = row.find_all('td')
                cols = [ele.text.strip().replace("\n\n", "") for ele in cols]
                scores_fixed.append([ele for ele in cols if ele])

        if scoreboard is not None:
            rows = scoreboard.find_all('tr')
            for row in rows[1:]:  # Skip first header row
                cols = row.find_all('td')
                cols = [ele.text.strip().replace("\n\n", "") for ele in cols]
                scores.append([ele for ele in cols if ele])

        return GameState(
            inning=inning,
            pitcher=pitcher,
            batter=batter,
            base_wrap=base_wrap,
            strike=strike,
            ball=ball,
            out=out,
            scores=scores,
            scores_fixed=scores_fixed
        )

    return None


team_name_map = {
    '樂天桃猿': '樂天桃猿',
    '中信兄弟': '中信兄弟',
    '味全龍': '味全龍',
    '統一7-ELEVEn獅': '統一獅',
    '富邦悍將': '富邦悍將'
}

short_team = {
    '樂天桃猿': '樂天',
    '中信兄弟': '中信',
    '味全龍': '味全',
    '統一7-ELEVEn獅': '統一',
    '富邦悍將': '富邦'
}


@error_handler(Exception, logger=logger)
def crawl_game_score_plays(game: Game, wait: int = 0.5) -> List[Play]:
    page = get_page(game.game_live_url, wait)
    soup = BeautifulSoup(page, "html.parser")

    game_live_soup = soup.find("div", class_="InningPlays")
    innings = game_live_soup.findAll("section") if game_live_soup is not None else []

    game_play: List[Play] = []
    for scoring in innings:
        inning = scoring.find("header").find(text=True, recursive=False).strip()
        plays = scoring.findAll("div", class_="item play")
        for play in plays:
            play_desc = play.find("div", class_="desc").get_text()
            play_desc_clean = re.sub('\\s{2,}', ' ', play_desc).strip()
            score = play.find("div", class_="vs_box").get_text()

            # score = score.replace("富邦悍將", game.team_home)
            # score = score.replace("Rakuten Monkeys", game.team_away)
            score = score.replace("富邦悍將", "")
            score = score.replace("Rakuten Monkeys", "")
            score = score.strip().replace(" ", "")
            # score = f"{team_name_map[game.team_away]} {score} {team_name_map[game.team_home]}"
            game_play.append(
                Play(inning=inning, play=play_desc_clean, score=score)
            )

    return game_play


@error_handler(Exception, logger=logger)
def crawl_box_score_tables(game: Game,
                           wait: int = 0.5,
                           rt_list: bool = False,
                           url: str = None) -> Union[GameBox, List, None]:
    # with browser_lock:
    #     browser.get(game.game_url)
    #     time.sleep(wait)
    #     box = browser.find_element(By.CLASS_NAME, value="GameBoxDetail")
    #     tabs = box.find_element(By.CLASS_NAME, value="tabs")
    #     lis = tabs.find_elements(By.TAG_NAME, value="li")
    #     span = lis[-1].find_element(By.TAG_NAME, value="a")
    #     span.click()
    #
    #     # ActionChains(browser).move_to_element(span).double_click()
    #
    #     # browser.execute_script('arguments[0].click()', span)
    #
    #     # element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(span))
    #     # element.click()
    #     time.sleep(1)
    #     # page = browser.execute_script("return document.body.innerHTML;")
    #     # page = browser.find_element(By.TAG_NAME, "body")
    #     # print(page.text)
    #     # page = page.get_attribute('outerHTML')

    #     page = browser.page_source

    page = get_page(game.game_url, wait)
    if url is not None:
        page = get_page(url, wait)
    soup = BeautifulSoup(page, "html.parser")

    # title = soup.find("div", class_="DistTitle")
    # title = title.find("h3").get_text()

    hit_record_tables = soup.findAll("div", class_="RecordTable")
    tables = []
    for hit_record_table in hit_record_tables:
        hit_record_table = hit_record_table.find("tbody")

        data = []
        rows = hit_record_table.find_all('tr')
        for row in rows[1:]:  # Skip first header row
            cols = row.find_all('td')
            cols = [ele.text.strip().replace("\n", "").replace(" ", "") or "empty" for ele in cols]
            data.append([ele for ele in cols if ele])
        tables.append(data)

    if rt_list:
        return tables

    # Validation
    if len(tables) != 6:
        logger.info(f"crawl_box_score_tables: {tables}")
        return None

    away_bat_box = [Batter.from_list(b) for b in tables[1]]
    home_bat_box = [Batter.from_list(b) for b in tables[4]]
    away_pitch_box = [Pitcher.from_list(b) for b in tables[2]]
    home_pitch_box = [Pitcher.from_list(b) for b in tables[5]]

    day = game.game_time.replace("比賽中 ", "").rsplit(' ', 1)[0].strip()
    day = day.replace("保留", "").strip()
    # TODO: fix unconverted data remains:  保留
    d = datetime.strptime(day, "%B %d, %Y").strftime("%m/%d")

    game_title = f"{short_team[game.team_away]} vs {short_team[game.team_home]}".strip()
    return GameBox(game_url_postfix=game.game_url_postfix,
                   game_title=game_title,
                   game_time_int=d,
                   away_bat_box=away_bat_box,
                   home_bat_box=home_bat_box,
                   away_pitch_box=away_pitch_box,
                   home_pitch_box=home_pitch_box)


@error_handler(Exception, logger=logger)
def crawl_standings(wait: int = 0.5) -> (str, List[Team]):
    page = get_page(cpbl.CPBL_STANDING_URL, wait)
    soup = BeautifulSoup(page, "html.parser")

    title = soup.find("div", class_="DistTitle")
    title = title.find("h3").get_text()

    record_table = soup.find("div", class_="RecordTable")
    record_table = record_table.find("tbody")

    data = []
    rows = record_table.find_all('tr')
    for row in rows[1:]:  # Skip first header row
        cols = row.find_all('td')
        cols = [ele.text.strip().replace("\n\n", "") for ele in cols]
        data.append([ele for ele in cols if ele])

    # teams = [Team.from_list(d) for d in data]
    # teams = Standing(**{"teams": teams})

    return title, [Team.from_list(d) for d in data]


@error_handler(Exception, logger=logger)
def check_game_start(game_url: str, wait: int = 0.5) -> bool:
    page = get_page(game_url, wait)
    soup = BeautifulSoup(page, "html.parser")
    not_start = soup.find("div", class_="game_canceled")

    return not_start is None


@error_handler(Exception, tries=10, logger=logger)
def check_game_end(game_live_url: str, wait: int = 0.5) -> bool:
    page = get_page(game_live_url, wait)
    soup = BeautifulSoup(page, "html.parser")
    game_status_soup = soup.find("li", class_="actived")

    tag_soup = game_status_soup.find("div", class_="tag game_status")
    # Early return for special case "比賽暫停"
    if tag_soup is None:
        return False
    game_stats = tag_soup.get_text()
    return game_stats == "比賽結束"


def stream_scoring_play(game: Game, plays: List[Play]):
    headers = {"Authorization": f"Bearer {settings.TOKEN}"}
    payload = {
        "game_title": f"{short_team[game.team_away]}vs{short_team[game.team_home]}",
        "game_url_postfix": game.game_url_postfix,
        "scoring_play": json.loads(json.dumps(plays, default=vars))
    }
    response = requests.post(settings.API_BASE + "/line/notify/scoring_play",
                             json=payload,
                             headers=headers)

    if response.status_code == 400:
        logger.error(f"Status code 400: payload = {payload}")


def game_tracker(game: Game, args):
    logger.info(f"Start tracking: {game.game_url_postfix}")
    scoring_plays = [] if game.scoring_play is None else game.scoring_play
    logger.info(f"Start plays from {scoring_plays}")
    auto_verifier = AutoVerify()
    try:
        while True:
            # 0. verification
            auto_verifier.timebase_verify()

            # 1. Check game started
            if not check_game_start(game.game_url):
                time.sleep(60)
                continue

            # 2.1 Get game state
            game_state = crawl_game_state(game.game_url)
            if game_state is not None and not args.local:
                game_cache.update_one_game_state(game.game_url_postfix, game_state)
                logger.info(f"Game state: {game_state}")

            # 2.2 Get game box
            game_box = crawl_box_score_tables(game)
            if game_box is not None and not args.local:
                game_cache.update_game_box(game.game_url_postfix, game_box=game_box)

            # 3. Get Scoring plays
            tmp_scoring_plays: List[Play] = crawl_game_score_plays(game)
            if len(tmp_scoring_plays) > len(scoring_plays):
                new_scoring_plays = tmp_scoring_plays[len(scoring_plays):]
                logger.info(f"Game: {game.game_url}, New scoring play = {new_scoring_plays}")

                scoring_plays = tmp_scoring_plays
                # current_score = scoring_plays[-1].score.split(" ")

                updated_game = game
                # updated_game.current_score = "".join(current_score[3:6])
                updated_game.current_score = scoring_plays[-1].score
                updated_game.scoring_play = scoring_plays

                if not args.local:
                    stream_scoring_play(game, new_scoring_plays)
                    game_cache.update_one_game_data(updated_game)

            # 4. Check game end
            if check_game_end(game.game_live_url):
                logger.info(f"Game {game.game_url_postfix} ended.")
                last_game_state = game_cache.get_game_state(game.game_url_postfix)

                last_play = scoring_plays[-1]
                if last_play.play != "比賽結束":
                    last_play.play = "比賽結束"
                    last_play.inning = last_game_state.inning \
                        if last_game_state is not None else "9 下"

                    scoring_plays.append(last_play)

                    updated_game = game
                    updated_game.current_score = scoring_plays[-1].score
                    updated_game.scoring_play = scoring_plays
                    stream_scoring_play(game, [last_play])
                    game_cache.update_one_game_data(updated_game)
                break

            time.sleep(3 + randint(0, 7))

    except KeyboardInterrupt:
        browser.quit()
        logger.info("Gracefully shut down game_tracker, quit web driver")
    return


def standing_tracker():
    standings = game_cache.get_standings()
    auto_verifier = AutoVerify()
    try:
        while True:
            title, stands = crawl_standings()
            if standings[title] == stands:
                logger.info("standing not update yet.")
                time.sleep(60)
                continue
            elif standings[title] != stands and len(standings[title]) == len(stands):
                logger.info("standing update.")
                game_cache.update_standings(title, stands)
                break

            auto_verifier.timebase_verify()

    except KeyboardInterrupt:
        logger.info("Gracefully shut down standing_tracker")

    return


def restore_games(games: Dict[str, Game]):
    old_games = game_cache.get_games_info()
    if set(games.keys()).issubset(set(old_games.keys())):
        logger.info("Restoring on going games")
        return old_games
    else:
        logger.info("Initialize new games.")
        game_cache.init_data(games)
        game_cache.update_games_data(games)
        return games


def main(args):
    # 1. Get Today's Box url
    games = crawl_today_games_info()
    logger.info(f"Today's games: {games}")

    if not args.local:
        games = restore_games(games)

    # 2. Tracking today's games: only track the game that are not postponed
    games = {k: game for k, game in games.items() if "延賽" not in game.game_time}
    process_list = []
    for i, (k, game) in enumerate(games.items()):
        process_list.append(Process(target=game_tracker, args=(game, args,)))
        process_list[i].start()

    for i, game in enumerate(games):
        process_list[i].join()

    # 3. Update standing
    standing_tracker()
    auto_verify = AutoVerify()
    auto_verify.auto()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--time", action="store_true")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    arg = parse_args()

    if arg.time:
        t0 = time.time()
        main(arg)
        t1 = time.time()
        total = t1 - t0
        logger.info(f"Total Time: {total} sec")
        browser.quit()
    else:
        main(arg)
        browser.quit()
