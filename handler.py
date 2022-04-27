import os
import json
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
from flex import (
    flex_message_type_condition,
    today_game,
)
from data_controller import (
    get_game_title,
    update_broadcast_list,
)

ON_HEROKU = os.environ.get('ON_HEROKU', None)
config = {}

if ON_HEROKU is None:
    config = json.loads(Path('config.json').read_text())

line_blueprint = Blueprint('line_controller', __name__, )

line_bot_api = LineBotApi(config["channel_access_token"])
handler = WebhookHandler(config["channel_secret"])


@line_blueprint.route("/line", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # TODO: use logger
    # logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text = event.message.text
    game_titles = get_game_title()
    print("Today's game:", game_titles)
    quick_reply = QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label="今日賽事", text="今日賽事")),
            QuickReplyButton(action=MessageAction(label="文字轉播", text="文字轉播")),
            QuickReplyButton(action=MessageAction(label="即時比數", text="即時比數")),
        ])
    alt = "觀看更多"

    if text == "今日賽事":
        alt = "今日賽事"
        contents = today_game()

    elif text == "文字轉播":
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label=title, text=title))
                for i, title in enumerate(game_titles)
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f"想要轉播的場次?", quick_reply=quick_reply),
        )
        return

    elif text in game_titles:
        print(event)
        print("Add user:", event.source)
        update_broadcast_list(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f"開始轉播{text}")
        )
        return

    elif text == "即時比數":
        alt = "即時比數"
        contents = today_game()

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
