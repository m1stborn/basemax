import logging

from flask import Flask

from config import Setting
from line.liff_handler import liff_blueprint
from line.line_handler import line_blueprint

settings = Setting()

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.register_blueprint(line_blueprint)
app.register_blueprint(liff_blueprint)


if __name__ == "__main__":
    if settings.ON_HEROKU:
        app.run(host='0.0.0.0', debug=False, port=settings.PORT)
    else:
        app.run(debug=False)
