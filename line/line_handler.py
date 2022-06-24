import logging
from urllib.parse import urlencode

from flask import Blueprint, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    StickerMessage,
    TextSendMessage,
    QuickReplyButton,
    MessageAction,
    QuickReply,
)

from config import Setting
from line.game_flex import (
    flex_message_wrapper,
    match_contents,
    scoreboard_contents,
)
from line.standing_flex import (
    standing_content,
)
from line.line_notify_handler import get_auth_link
from models import game_cache

settings = Setting()
logger = logging.getLogger(__name__)

line_blueprint = Blueprint('line', __name__, )

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)


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
        QuickReplyButton(action=MessageAction(label="連結Notify", text="連結Notify")),
    ]
)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text

    game_titles = game_cache.get_game_title()
    game_titles_to_url = {v: k for k, v in game_titles.items()}

    logger.info(f"Message Event = {event}")
    alt = "觀看更多"

    quick_reply = default_quick_reply

    if text == "今日賽事":
        alt = "今日賽事"
        contents = match_contents()
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
        game_cache.update_broadcast_list(game_titles_to_url[text], event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f"開始轉播{text}", quick_reply=quick_reply)
        )
        return

    elif text == "即時比數":
        contents = scoreboard_contents()
        if len(contents) == 0:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text="目前無進行中的賽事", quick_reply=quick_reply)
            )
            return

    elif text == "球隊戰績":
        contents = standing_content()

    elif text == "連結Notify":
        # TODO: get line_id by func, should support group_id in future
        query_string = {
            'state': event.source.user_id
        }
        url = f"{settings.API_BASE}/line/notify?{urlencode(query_string)}"
        reply_text = f"請至以下網址連動LINE NOTIFY與CPBLbot:\n{url}"

        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=reply_text, quick_reply=quick_reply)
        )
        return

    else:
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f"需要我做什麼呢?", quick_reply=quick_reply)
        )
        return

    flex = flex_message_wrapper(alt, contents, quick_reply=quick_reply)

    line_bot_api.reply_message(
        event.reply_token,
        messages=flex
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        messages=TextSendMessage(text=f"需要我做什麼呢?", quick_reply=default_quick_reply)
    )


@line_blueprint.route("/game/scoring_play", methods=['POST'])
def handle_scoring_play():
    scoring_play_obj = request.get_json()
    game_url = scoring_play_obj.get("game_url_postfix")
    scoring_play = scoring_play_obj.get("scoring_play")
    user_id_list = game_cache.get_broadcast_list(game_url)
    for play in scoring_play:
        text = "\n\n".join(play.values())
        line_bot_api.multicast(user_id_list, TextSendMessage(text=text, quick_reply=default_quick_reply))

    return 'OK'
