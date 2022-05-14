import json
import logging
import os
from pathlib import Path
from typing import Dict

from flask import request, Blueprint, Response, render_template, abort

from line.game_flex import flex_message_wrapper
from line.standing_flex import (
    standing_content,
)

logger = logging.getLogger(__name__)

ON_HEROKU = os.environ.get('ON_HEROKU', None)
if ON_HEROKU:
    LIFF_ID = os.getenv('LIFF_SHARE_ID')
else:
    config = json.loads(Path('./config.json').read_text())
    LIFF_ID = config["LIFF_SHARE_ID"]

liff_blueprint = Blueprint('liff', __name__, template_folder="./templates")


@liff_blueprint.route("/liff/share", methods=['GET'])
def liff_page():
    print(f"Query string: {request.args}")
    logger.info(f"Query string: {request.args}")
    # if request.args.get("life.state"):
    #     return Response(render_template('liff_redirect.html', liff_id=LIFF_ID))
    return Response(render_template('liff_redirect.html', liff_id=LIFF_ID))


@liff_blueprint.route("/liff/share/standing", methods=['GET'])
def liff_share_standing():
    alt = "分享CPBL戰績排行"
    # alt = "CPBL球隊戰績"
    contents = standing_content(footer=False)
    flex = flex_json(alt, contents)

    return Response(render_template('share_message.html', flex=flex, liff_id=LIFF_ID))


def flex_json(alt: str, content: Dict):
    return {
        "type": "flex",
        "altText": alt,
        "contents": {
            **{
                "type": "carousel",
                "contents": [content]
            }
        }
    }
