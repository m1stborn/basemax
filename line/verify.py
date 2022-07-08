import logging
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

import jwt
import requests

from config import Setting

settings = Setting()
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@dataclass
class AutoVerify:
    last_verify_time: datetime = None

    def __post_init__(self):
        self.last_verify_time = datetime.now()

    @staticmethod
    def verify():
        payload = {
            "sub": "cpblbot-heroku",
            "name": "m1stborn",
            "token": str(uuid.uuid4())[:8]
        }
        jwt_token = jwt.encode(payload, settings.CPBLBOT_SECRET_KEY, algorithm='HS256')
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.post(settings.API_BASE + "/line/notify/scoring_play",
                                 headers=headers)

        if response.status_code == 400:
            logger.error(f"Status code 400: payload = {payload}")

        return response.json()

    def timebase_verify(self, delta: 5):
        if datetime.now() - self.last_verify_time > timedelta(seconds=delta*60):
            self.last_verify_time = datetime.now()
            return self.verify()

    def auto(self, delta: 5):
        while True:
            time.sleep(delta * 60)
            if datetime.now() - self.last_verify_time > timedelta(seconds=delta*60):
                self.last_verify_time = datetime.now()
                response = self.verify()
                logger.info(f"response: {response}")
