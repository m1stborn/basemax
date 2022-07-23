import logging
from typing import Dict, List, Union

from flask import (
    request,
    Blueprint,
    Response,
    render_template,
    abort,
    current_app
)
from werkzeug.local import LocalProxy

from config import Setting
from line.pitching_box_flex import pitching_box_contents
from models import game_cache
from line.batting_box_flex import batting_box_contents
from line.game_flex import (
    scoreboard_contents,
    match_contents,
)
from line.standing_flex import (
    standing_contents,
)
from line.scoreboard_flex import scoreboard_innings_contents

settings = Setting()
logger = LocalProxy(lambda: current_app.logger)

liff_blueprint = Blueprint('liff', __name__, )


@liff_blueprint.route("/liff/share", methods=['GET'])
def liff_page():
    if request.args.get("liff.state"):
        return Response(render_template('liff_redirect.html', liff_id=settings.LIFF_SHARE_ID))

    abort(404)


@liff_blueprint.route("/liff/share/<string:action>", methods=['GET'])
def liff_share_standing(action):

    # TODO: add me flex for default
    alt = "分享CPBL戰績排行"
    contents = standing_contents(footer=False)
    flex = flex_json(alt, contents)

    if action == "standing":
        alt = "分享CPBL戰績排行"
        contents = standing_contents(footer=False)
        flex = flex_json(alt, contents)

    elif action == "match":
        alt = "分享CPBL今日賽事"
        contents = match_contents(footer=False)
        flex = flex_json(alt, contents)

    elif action == "score":
        alt = "分享CPBL即時比數"
        # contents = scoreboard_contents(footer=False)
        contents = scoreboard_innings_contents(footer=False)
        flex = flex_json(alt, contents)

    elif action == "batbox":
        alt = "分享CPBL boxscore"
        game_idx = request.args.get('gameSno')
        boxes = game_cache.get_game_boxes()
        game_uid_matches = [key for key, value in boxes.items() if game_idx in key]
        logger.info(f'batbox {game_uid_matches}')
        if len(game_uid_matches) < 0:
            return abort(400)
        contents = batting_box_contents(game_uid=game_uid_matches[-1], footer=False)
        flex = flex_json(alt, contents)

    elif action == "pitchbox":
        alt = "分享CPBL boxscore"
        game_idx = request.args.get('gameSno')
        boxes = game_cache.get_game_boxes()
        game_uid_matches = [key for key, value in boxes.items() if game_idx in key]
        logger.info(f'pitchbox {game_uid_matches}')
        if len(game_uid_matches) < 0:
            return abort(400)
        contents = pitching_box_contents(game_uid=game_uid_matches[-1], footer=False)
        flex = flex_json(alt, contents)

    return Response(render_template('share_message.html', flex=flex, liff_id=settings.LIFF_SHARE_ID))


def flex_json(alt: str, content: Union[Dict, List[Dict]]):
    if isinstance(content, dict):
        content = [content]
    return {
        "type": "flex",
        "altText": alt,
        "contents": {
            **{
                "type": "carousel",
                "contents": content
            }
        }
    }
