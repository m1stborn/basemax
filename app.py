import logging

from flask import Flask

from config import Setting
from line.liff_handler import liff_blueprint
from line.line_handler import line_blueprint
from line.line_notify_handler import line_notify_blueprint

settings = Setting()

app = Flask(__name__, static_folder="./line/templates/static", template_folder="./line/templates")
app.logger.setLevel(logging.INFO)
app.register_blueprint(line_blueprint)
app.register_blueprint(liff_blueprint)
app.register_blueprint(line_notify_blueprint)


if __name__ == "__main__":
    if settings.ON_HEROKU:
        app.logger.info("Start heroku server")
        app.run(host='0.0.0.0', debug=True, port=settings.PORT)
    else:
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(debug=True, host='0.0.0.0')
