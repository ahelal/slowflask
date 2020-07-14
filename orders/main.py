#!/usr/bin/env python3
from flask import Flask
from flask import jsonify
from flask import request
import time
from datetime import datetime
import os
import sys
import multiprocessing
from pathlib import Path
import tempfile
import shutil
from filelock import FileLock

app = Flask(__name__)

def inc_order():
    orders = 0
    with FileLock("orders.txt.lock"):
        try:
            with open("orders.txt") as r:
                orders = r.readline()
        except FileNotFoundError:
            pass
        orders = int(orders) + 1
        with open("orders.txt", 'w') as f:
            f.write(str(orders))
        return orders

def processfile(file_path=None,size=60):
    with open(file_path, 'w') as f:
        mb = int((size*2**20)//512)
        # write file
        for i in range(mb):
            f.write(str(os.urandom(512)))
        # read file
        with open(file_path, 'rb') as reader:
            reader.readline()

def processes_order():
    temp_dir = tempfile.TemporaryDirectory(dir=Path.home())
    file_path = temp_dir.name + "/f"
    processfile(file_path)
    r = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    while r < 1300:
        r = r + 0.512 / r
    return inc_order()

@app.route("/")
def root():
    return "Welcome!"

@app.route("/order")
def order():
    orders = processes_order()
    return jsonify({"Order": orders})

@app.route("/health")
def health():
    return jsonify({"API": True})

if __name__ == "__main__":
    i = 0
    cores = multiprocessing.cpu_count()
    cores = 1
    app.run(host= '0.0.0.0', port=8080, debug=True, processes=cores,threaded=False)
