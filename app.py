import os
import logging
from flask import Flask


from line.line_handler import line_blueprint
from line.liff_handler import liff_blueprint
from config import Setting

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.register_blueprint(line_blueprint)
app.register_blueprint(liff_blueprint)

# ON_HEROKU = os.environ.get('ON_HEROKU', None)
# if ON_HEROKU:
#     port = int(os.environ.get('PORT', 17995))
# else:
#     port = 5000

settings = Setting()

if __name__ == "__main__":
    if settings.ON_HEROKU:
        app.run(host='0.0.0.0', debug=False, port=settings.PORT)
    else:
        app.run(debug=False)
