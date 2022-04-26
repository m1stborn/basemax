import re
import time
from typing import List, Dict, Union

from bs4 import BeautifulSoup
from requests_html import HTMLSession

EMPTY_LINK = 'javascript:;'

url_base = "https://www.cpbl.com.tw"
url = "https://www.cpbl.com.tw/schedule"


def get_today_game_url() -> (List[str]):
    session = HTMLSession()
    response = session.get(url, verify=False)
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, "lxml")
    # TODO: add date
    day_soup = soup.find('div', class_='date', attrs={'data-date': "26"})
    result = day_soup.parent.findAll('a') if day_soup is not None else []
    game_link_postfix = [game['href'] for game in result if game['href'] != EMPTY_LINK]

    game_url = [url_base + link for link in game_link_postfix]
    game_live_url = [url_base + link.replace('/box', '/box/live') for link in game_link_postfix]
    game_index_url = [url_base + link.replace('/box', '/box/index') for link in game_link_postfix]

    # return game_url, game_live_url, game_index_url
    return game_link_postfix


def get_game_info(game_live_url: str) -> Dict:
    session = HTMLSession()

    response = session.get(game_live_url, verify=False)
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, "lxml")
    game_live_soup = soup.find("div", class_="item ScoreBoard")
    team_away = game_live_soup.find("div", class_="team away").find("div", class_="team_name").get_text()
    team_home = game_live_soup.find("div", class_="team home").find("div", class_="team_name").get_text()

    # team_away = soup.find("div", class_="team away").get_text()
    # team_home = soup.find("div", class_="team home").get_text()

    return {
        "team_away": team_away,
        "team_home": team_home,
    }


def get_game_score_plays(game_live_url: str, game_info: Dict) -> List[Dict]:
    session = HTMLSession()

    response = session.get(game_live_url, verify=False)
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

            score.replace("Rakuten Monkeys", game_info["team_away"])
            score.replace("富邦悍將", game_info["team_home"])

            game_play.append({
                "inning": inning,
                "play": play_desc_clean,
                "score": score,
            })
        # print(inning, play_desc_clean, score)
        # play_desc2 = play.find("div", class_="desc").findAll(text=True)
        # print(inning, play_desc)
        # print(inning, "".join([play.replace('\n').strip() for play in play_desc2]))
    return game_play


def check_game_start(game_url: str) -> bool:
    session = HTMLSession()
    response = session.get(game_url, verify=False)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, "lxml")

    not_start = soup.find("div", class_="game_canceled")

    return not_start is None


def check_game_end(game_index_url: str) -> bool:
    session = HTMLSession()
    response = session.get(game_index_url, verify=False)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, "lxml")

    # game_brief = soup.find("div", class_="GameNote")
    game_brief = soup.find("div", class_="editable_content")

    return game_brief is not None


# def game_tracker():
#     try:
#         while True:
#             # Check game started
#             if check_game_start(game_url[1]):
#                 scoring_plays = []
#                 while True:
#                     tmp_scoring_plays = get_game_score_plays(game_live_link[1], game_info)
#                     if len(tmp_scoring_plays) > len(scoring_plays):
#                         print(tmp_scoring_plays[len(scoring_plays):])
#                         scoring_plays = tmp_scoring_plays
#                     if check_game_end(game_index_url[1]):
#                         break
#                     time.sleep(60)
#             if check_game_end(game_index_url[1]):
#                 break
#
#     except KeyboardInterrupt:
#         pass


def main():
    # 1. Get Today's Box url
    # game_url, game_live_link, game_index_url = get_today_game_url()
    game_link_postfix = get_today_game_url()

    game_url = [url_base + link for link in game_link_postfix]
    game_live_link = [url_base + link.replace('/box', '/box/live') for link in game_link_postfix]
    game_index_url = [url_base + link.replace('/box', '/box/index') for link in game_link_postfix]

    game_info = get_game_info(game_live_link[1])

    # 2. Get box live
    try:
        while True:
            # Check game started
            if check_game_start(game_url[1]):
                scoring_plays = []
                while True:
                    tmp_scoring_plays = get_game_score_plays(game_live_link[1], game_info)
                    if len(tmp_scoring_plays) > len(scoring_plays):
                        print(tmp_scoring_plays[len(scoring_plays):])
                        scoring_plays = tmp_scoring_plays
                    if check_game_end(game_index_url[1]):
                        break
                    time.sleep(60)
            if check_game_end(game_index_url[1]):
                break

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
