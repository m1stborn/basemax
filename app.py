import os
import logging
from flask import Flask


from line.handler import line_blueprint

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.register_blueprint(line_blueprint)

ON_HEROKU = os.environ.get('ON_HEROKU', None)
if ON_HEROKU:
    port = int(os.environ.get('PORT', 17995))
else:
    port = 5000

if __name__ == "__main__":
    if ON_HEROKU:
        app.run(host='0.0.0.0', debug=False, port=port)
    else:
        app.run(debug=False)
