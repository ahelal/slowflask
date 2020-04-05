#!/usr/bin/env python3
from flask import Flask
from multiprocessing import Pool
from multiprocessing import cpu_count
from datetime import datetime
app = Flask(__name__)

def f(x):
    start_time = datetime.now()
    while True:
        x*x
        time_delta = datetime.now() - start_time
        if time_delta.total_seconds() >= 5:
            break
    
@app.route("/")
def hello():
    processes = cpu_count()
    pool = Pool(processes)
    pool.map(f, range(processes))
    return "Hello World!"

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=8080)