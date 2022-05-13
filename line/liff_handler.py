import json
import os
from pathlib import Path

from flask import Blueprint, Response, render_template

from line.game_flex import flex_message_wrapper
from line.standing_flex import (
    standing_content,
)

ON_HEROKU = os.environ.get('ON_HEROKU', None)
if ON_HEROKU:
    LIFF_ID = os.getenv('LIFF_SHARE_ID')
else:
    config = json.loads(Path('./config.json').read_text())
    LIFF_ID = config["LIFF_SHARE_ID"]

liff_blueprint = Blueprint('liff', __name__, template_folder="./templates")


@liff_blueprint.route("/liff/share/liff.state", methods=['get'])
def liff_state_handler():
    return Response(render_template('liff_redirect.html', liff_id=LIFF_ID))


@liff_blueprint.route("/liff/share/standing", methods=['get'])
def liff_handler():
    alt = "分享CPBL戰績排行"
    contents = standing_content(footer=False)
    flex = flex_message_wrapper(alt, contents)

    # elif stream:
    #     alt = "CPBL球隊戰績"
    #     content.append(stream_flex_template(row.id, row.title, row.image, row.link))
    # else:
    #     content = [add_me()]
    # return msg, LIFF_ID
    return Response(render_template('share_message.html', flex=flex, liff_id=LIFF_ID))

