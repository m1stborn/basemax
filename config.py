import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

from pydantic import BaseSettings, BaseModel


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    return json.loads(Path('config.json').read_text())


class Setting(BaseSettings):
    # Heroku
    ON_HEROKU: bool
    PORT: int
    API_BASE: str

    # Redis
    REDIS_URL: str
    REDIS_TLS_URL: Optional[str]

    # Postgresql
    DB_URI: str

    # Line
    CHANNEL_ACCESS_TOKEN: str
    CHANNEL_SECRET: str
    LIFF_SHARE_ID: str

    # Line notify
    LINE_NOTIFY_CLIENT_ID: str
    LINE_NOTIFY_CLIENT_SECRET: str

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


class CPBLSetting(BaseModel):
    EMPTY_LINK: str = "javascript:;"
    CPBL_BASE_URl: str = "https://www.cpbl.com.tw"
    CPBL_SCHEDULE_URL: str = "https://www.cpbl.com.tw/schedule"
    CPBL_STANDING_URL: str = "https://www.cpbl.com.tw/standings/season"
