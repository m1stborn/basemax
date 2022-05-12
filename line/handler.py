import os
import json
import logging
from pathlib import Path

from flask import Blueprint, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    QuickReplyButton,
    MessageAction,
    QuickReply,
)

from line.flex import (
    flex_message_type_condition,
    today_game,
    current_score,
)
from line.standing_flex import (
    standing_content,
)
from models import game_mod

logger = logging.getLogger(__name__)

ON_HEROKU = os.environ.get('ON_HEROKU', None)
if ON_HEROKU:
    LINE_CHANNEL_SECRET = os.environ.get('channel_secret', None)
    LINE_ACCESS_TOKEN = os.environ.get('channel_access_token', None)
else:
    config = json.loads(Path('./config.json').read_text())
    LINE_CHANNEL_SECRET = config["channel_secret"]
    LINE_ACCESS_TOKEN = config["channel_access_token"]

line_blueprint = Blueprint('line', __name__, )

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@line_blueprint.route("/line", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


default_quick_reply = QuickReply(
    items=[
        QuickReplyButton(action=MessageAction(label="今日賽事", text="今日賽事")),
        QuickReplyButton(action=MessageAction(label="文字轉播", text="文字轉播")),
        QuickReplyButton(action=MessageAction(label="即時比數", text="即時比數")),
        QuickReplyButton(action=MessageAction(label="球隊戰績", text="球隊戰績")),
    ]
)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    game_titles = game_mod.get_game_title()
    game_titles_to_url = {v: k for k, v in game_titles.items()}

    logger.info(f"Message Event = {event}")
    alt = "觀看更多"

    quick_reply = default_quick_reply

    if text == "今日賽事":
        alt = "今日賽事"
        contents = today_game()
        if len(contents) == 0:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text="今日中職沒有比賽", quick_reply=quick_reply)
            )
            return

    elif text == "文字轉播":
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label=title, text=title))
                for i, (url, title) in enumerate(game_titles.items())
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f"想要轉播的比賽?", quick_reply=quick_reply),
        )
        return

    elif text in game_titles.values():
        game_mod.update_broadcast_list(game_titles_to_url[text], event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f"開始轉播{text}", quick_reply=quick_reply)
        )
        return

    elif text == "即時比數":
        contents = current_score()
        if len(contents) == 0:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text="目前無進行中的賽事", quick_reply=quick_reply)
            )
            return
    elif text == "球隊戰績":
        contents = standing_content()
    else:
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f"需要我做什麼呢?", quick_reply=quick_reply)
        )
        return

    flex = flex_message_type_condition(alt, contents, quick_reply=quick_reply)

    line_bot_api.reply_message(
        event.reply_token,
        messages=flex
    )


@line_blueprint.route("/game/scoring_play", methods=['POST'])
def handel_scoring_play():
    scoring_play_obj = request.get_json()
    game_url = scoring_play_obj.get("game_url_postfix")
    scoring_play = scoring_play_obj.get("scoring_play")
    user_id_list = game_mod.get_broadcast_list(game_url)
    for play in scoring_play:
        text = "\n\n".join(play.values())
        line_bot_api.multicast(user_id_list, TextSendMessage(text=text, quick_reply=default_quick_reply))

    return 'OK'