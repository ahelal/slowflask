#!/usr/bin/env python3
from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)

def f(x):
    start_time = datetime.now()
    while True:
        x*x
        time_delta = datetime.now() - start_time
        if time_delta.total_seconds() >= 1:
            break

@app.route("/")
def hello():
    r = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    f(r)
    return "Hello World!"

@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=8080)
