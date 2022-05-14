import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

from pydantic import BaseSettings, BaseModel


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    return json.loads(Path('config.json').read_text())


class Setting(BaseSettings):
    ON_HEROKU: str
    HEROKU_BASE: str
    LIFF_SHARE_ID: str
    REDIS_URL: str
    CHANNEL_ACCESS_TOKEN: str
    CHANNEL_SECRET: str
    PORT: int
    REDIS_TLS_URL: Optional[str]

    class Config:

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            if os.environ.get('ON_HEROKU', None):
                return (
                    init_settings,
                    env_settings,
                    file_secret_settings,
                )
            return (
                json_config_settings_source,
            )


class CrawlerSetting(BaseModel):
    EMPTY_LINK: str = "javascript:;"
    CPBL_BASE_URl: str = "https://www.cpbl.com.tw"
    CPBL_SCHEDULE_URL: str = "https://www.cpbl.com.tw/schedule"
    CPBL_STANDING_URL: str = "https://www.cpbl.com.tw/standings/season"


if __name__ == '__main__':
    config = CrawlerSetting()
    dev_config = Setting()
    print(dev_config)
    print(config.CPBL_BASE_URl)
