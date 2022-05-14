import json
import os
from pathlib import Path
from typing import Dict

ON_HEROKU = os.environ.get('ON_HEROKU', None)
if ON_HEROKU:
    LIFF_ID = os.getenv('LIFF_SHARE_ID')
else:
    config = json.loads(Path('./config.json').read_text())
    LIFF_ID = config["LIFF_SHARE_ID"]

CPBL_URL = "https://www.cpbl.com.tw"
SHARE_URL = f"https://liff.line.me/{LIFF_ID}"
# SHARE_STANDING_URL = f"https://liff.line.me/{LIFF_ID}/standing"


def footer_flex(main_link: str = CPBL_URL,
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
