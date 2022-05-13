from typing import Dict


def footer_flex(main_link: str, share_link: str) -> Dict:
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
                    "uri": share_link
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
