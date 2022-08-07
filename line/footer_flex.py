from typing import Dict

from config import Setting, CPBLSetting

settings = Setting()
cpbl = CPBLSetting()

SHARE_URL = f"https://liff.line.me/{settings.LIFF_SHARE_ID}"


def footer_flex(main_link: str = cpbl.CPBL_BASE_URl,
                # share_link: str = SHARE_STANDING_URL,
                post_fix: str = "/standing") -> Dict:
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "官方網站",
                    "uri": main_link
                },
                "height": "sm",
                "style": "secondary",
                "offsetStart": "md",
                "offsetBottom": "sm",
                "flex": 10
            },
            {
                "type": "filler",
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "分享",
                    "uri": f"{SHARE_URL}{post_fix}"
                },
                "style": "primary",
                "height": "sm",
                "margin": "xl",
                "offsetBottom": "sm",
                "offsetEnd": "md",
                "flex": 10,
                "color": "#9fa8da"
            }
        ]
    }


def share_footer_flex(main_link: str = cpbl.CPBL_BASE_URl,
                      add_line: str = "https://line.me/R/ti/p/@591tovcw") -> Dict:
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "官方網站",
                    "uri": main_link
                },
                "height": "sm",
                "style": "secondary",
                "offsetStart": "md",
                "offsetBottom": "sm",
                "flex": 10
            },
            {
                "type": "filler",
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "加入好友",
                    "uri": f"{add_line}"
                },
                "style": "primary",
                "height": "sm",
                "margin": "xl",
                "offsetBottom": "sm",
                "offsetEnd": "md",
                "flex": 10,
                "color": "#9fa8da"
            }
        ]
    }
