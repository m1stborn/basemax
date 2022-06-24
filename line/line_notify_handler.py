import logging
import uuid
from urllib.parse import urlencode

import requests
from flask import Blueprint, request, render_template

from config import Setting
from models import game_cache

logger = logging.getLogger(__name__)
settings = Setting()

line_notify_blueprint = Blueprint('line_notify', __name__, )

REDIRECT_URI = f"{settings.API_BASE}/line/notify/confirm"
NOTIFY_BOT_URL = "https://notify-bot.line.me"


@line_notify_blueprint.route("/")
def handle_index():
    return render_template("line_notify_index.html")


@line_notify_blueprint.route("/line/notify")
def handle_line_notify():
    link = get_auth_link(state=uuid.uuid4())
    logger.info(f"handle_line_notify-link: {link}")
    return render_template("line_notify_index.html", auth_url=link)


@line_notify_blueprint.route("/line/notify/confirm")
def handle_confirm():
    token = get_access_token(code=request.args.get("code"))
    logger.info(f"New Line Notify user: {token}")
    # TODO: successful template
    return "Connect to Line Notify Successful!"


@line_notify_blueprint.route("/line/notify/scoring_play", methods=["POST"])
def send():
    scoring_play_obj = request.get_json()
    game_url = scoring_play_obj.get("game_url_postfix")
    scoring_play = scoring_play_obj.get("scoring_play")
    user_id_list = game_cache.get_broadcast_list(game_url)
    for play in scoring_play:
        text = "\n\n".join(play.values())
        # line_bot_api.multicast(user_id_list, TextSendMessage(text=text, quick_reply=default_quick_reply))
        logger.info(f"New scoring play: {text}")
        # send_notify(text, "access_token")


def get_auth_link(state):
    query_string = {
        'scope': 'notify',
        'response_type': 'code',
        'client_id': settings.LINE_NOTIFY_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': state
    }

    return '{url}/oauth/authorize?{query_string}'.format(
        url=NOTIFY_BOT_URL, query_string=urlencode(query_string))


def get_access_token(code):
    response = requests.post(
        url=f"{NOTIFY_BOT_URL}/oauth/token",
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': settings.LINE_NOTIFY_CLIENT_ID,
            'client_secret': settings.LINE_NOTIFY_CLIENT_SECRET
        })
    if 200 <= response.status_code < 300:
        pass
    elif response.status_code == 400:
        logger.error("Status code 400: get_access_token")
    # try:
    #     response = requests.post(
    #         url, headers=headers, data=data, files=files, timeout=timeout)
    #     self.__check_http_response_status(response)
    #     self.__check_http_response_status(response)
    #     return response
    # except requests.exceptions.Timeout:
    #     raise RuntimeError(
    #         'Request time {timeout} timeout. Please check internet.'.format(timeout=timeout)
    #     )
    # except requests.exceptions.TooManyRedirects:
    #     raise RuntimeError('URL {url} was bad, please try a different one.'.format(url=url))
    return response.json().get('access_token')


def send_notify(message: str, access_token: str, notification_disabled: bool = False):
    params = {'message': message}
    if notification_disabled:
        params.update({'notificationDisabled': notification_disabled})

    response = requests.post(
        url=f'{NOTIFY_BOT_URL}/api/notify',
        data=params,
        headers={
            'Authorization': 'Bearer {token}'.format(token=access_token)
        })
    if response.status_code == 400:
        logger.error(f"Status code 400: send_notify")
