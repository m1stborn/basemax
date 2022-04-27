import os
import time
import multiprocessing as mp

import schedule
from flask import Flask

from crawler import main
from handler import line_blueprint

app = Flask(__name__)
app.register_blueprint(line_blueprint)

ON_HEROKU = os.environ.get('ON_HEROKU', None)

if ON_HEROKU:
    port = int(os.environ.get('PORT', 17995))
else:
    port = 3000


def parallelize_functions(*functions):
    processes = []
    for function in functions:
        p = mp.Process(target=function)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def track():
    print("Start tracking CPBL")
    main()
    # schedule.every().day.at("14:47").do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


def run_app():
    app.run(debug=False)


if __name__ == "__main__":
    # parallelize_functions(run_app, track)
    app.run(host='0.0.0.0', debug=False, port=port)
