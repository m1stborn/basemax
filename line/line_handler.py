import logging
from urllib.parse import urlencode

from flask import Blueprint, request, abort, current_app
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    FollowEvent,
    TextMessage,
    StickerMessage,
    TextSendMessage,
    QuickReplyButton,
    MessageAction,
    QuickReply,
)
from werkzeug.local import LocalProxy

from config import Setting
from line.batting_box_flex import batting_box_contents
from line.pitching_box_flex import pitching_box_contents
from line.game_flex import (
    flex_message_wrapper,
    match_contents,
)
from line.scoreboard_flex import scoreboard_innings_contents
from line.standing_flex import (
    standing_contents,
)
from line.line_notify_handler import get_auth_link
from models import game_cache, line_user

settings = Setting()
logger = LocalProxy(lambda: current_app.logger)

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
        QuickReplyButton(action=MessageAction(label="box", text="box")),
        QuickReplyButton(action=MessageAction(label="球隊戰績", text="球隊戰績")),
        # QuickReplyButton(action=MessageAction(label="連結Notify", text="連結Notify")),
    ]
)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text

    game_titles = game_cache.get_game_title()
    game_title_to_url = {v: k for k, v in game_titles.items()}
    batting_box_to_url = {f"{v}[打擊]": k for k, v in game_titles.items()}  # keys: <game>[打擊] # value: game_uid
    pitching_box_to_url = {f"{v}[投手]": k for k, v in game_titles.items()}  # keys: <game>[投手] # value: game_uid

    # TODO: only put available box to list
    # boxes = game_cache.get_game_boxes()
    box_to_url = {**batting_box_to_url, **pitching_box_to_url}

    logger.info(f"box_qr: {batting_box_to_url}, {pitching_box_to_url}")
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
        reply_text = "想要轉播的比賽?"
        if not line_user.check_notify_connect(event.source.user_id):
            append_text = get_notify_connect_reply(event.source.user_id)
            reply_text = f"{append_text}\n{reply_text}"

        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=reply_text, quick_reply=quick_reply),
        )
        return

    elif text in game_titles.values():
        user = line_user.get_user_by_id(event.source.user_id)
        game_cache.update_broadcast_list(game_title_to_url[text], user.line_notify_access_token)

        # Now the broadcast_list caching to notify token, not user_id anymore.
        user = line_user.get_user_by_id(event.source.user_id)
        logger.info(f"Get user: {user}")
        game_cache.update_broadcast_list(game_title_to_url[text], user.line_notify_access_token)
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f"開始轉播{text}", quick_reply=quick_reply)
        )
        return

    elif text == "box":
        quick_reply = QuickReply(
            items=[QuickReplyButton(action=MessageAction(label=k, text=k))
                   for k in box_to_url.keys()]
        )
        reply_text = "想要查看的box?"

        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=reply_text, quick_reply=quick_reply),
        )
        return

    elif text in batting_box_to_url.keys():
        game_uid = batting_box_to_url[text]
        contents = batting_box_contents(game_uid)
        if len(contents) == 0:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text="比賽尚未開始", quick_reply=quick_reply)
            )
            return

    elif text in pitching_box_to_url.keys():
        game_uid = pitching_box_to_url[text]
        contents = pitching_box_contents(game_uid)
        if len(contents) == 0:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text="比賽尚未開始", quick_reply=quick_reply)
            )
            return

    elif text == "即時比數":
        contents = scoreboard_innings_contents()
        if len(contents) == 0:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text="目前無進行中的賽事", quick_reply=quick_reply)
            )
            return

    elif text == "球隊戰績":
        contents = standing_contents()

    elif text == "連結Notify":
        # TODO: get line_id by func, should support group_id in future
        reply_text = get_notify_connect_reply(event.source.user_id)
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


@handler.add(FollowEvent)
def handle_sticker_message(event):
    query_string = {
        'state': event.source.user_id
    }
    url = f"{settings.API_BASE}/line/notify?{urlencode(query_string)}"
    welcome_message = f"""歡迎使用 CPBLBot 中職機器人!
請按以下步驟連接 LINE Notify 以啟用文字轉播功能。
1. 開啟下方網址
2. 選擇第一個「透過1對1聊天接收LINE Notify的通知」
3. 點擊「同意並連動」
{url}
連動成功後即可在Line Notify聊天室中接收文字轉播!

你將能使用這些功能: 今日賽事、文字轉播、即時比數、box、球隊戰績!
(若未連結Line Notify則無法使用文字轉播)
"""
    line_bot_api.reply_message(
        event.reply_token,
        messages=TextSendMessage(text=welcome_message, quick_reply=default_quick_reply)
    )

    # TODO: get user display name
    # example
    # from linebot import LineBotApi
    # from linebot.exceptions import LineBotApiError
    #
    # line_bot_api = LineBotApi('<channel access token>')
    #
    # try:
    #     profile = line_bot_api.get_profile('<user_id>')
    # except LineBotApiError as e:
    #     # error handle


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


def get_notify_connect_reply(line_id: str) -> str:
    query_string = {
        'state': line_id
    }
    url = f"{settings.API_BASE}/line/notify?{urlencode(query_string)}"
    reply_text = f"第一次使用文字轉播請至以下網址連結LINE NOTIFY與CPBLbot:\n{url}\n" \
                 f"連結成功後即可在Line Notify聊天室中接收文字轉播!"
    return reply_text
