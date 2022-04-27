import multiprocessing as mp
import time

import schedule
from flask import Flask

from crawler import main
from handler import line_blueprint

app = Flask(__name__)
app.register_blueprint(line_blueprint)


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
    app.run(debug=False)