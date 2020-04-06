#!/usr/bin/env python3
from flask import Flask
from multiprocessing import Pool
from multiprocessing import cpu_count
import multiprocessing

app = Flask(__name__)

def f(x):
    while True:
        x*x

def multi_proc():
    processes = cpu_count()
    pool = Pool(processes)
    pool.map(f, range(processes))

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    p = multiprocessing.Process(target=multi_proc)
    p.start()

    app.run(host= '0.0.0.0', port=8080)
