#!/usr/bin/env python3

from flask import Flask
from flask import jsonify
from flask import request
from markupsafe import escape
from functools import reduce
import os
import threading
import time
import operator
import json
import os.path
from os import path

lock = threading.Condition()
app = Flask(__name__)
DB = {}
DB_UPDATED = False
BACKUP_FILE="/tmp/backend.json"

def get_from_dict(data_dict, map_list):
    return reduce(operator.getitem, map_list, data_dict)

def set_in_dict(data_dict, map_list, value):
    get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value
    return get_from_dict(data_dict, map_list)

def read_from_db(database, path):
    path_list = list(filter(None, path.split("/")))
    if len(path_list) == 0 or database is None or database == {}:
        return None
    try :
        result = get_from_dict(database, path_list)
    except KeyError:
        result = None
    return result

def write_to_db(database, path, value):
    path_list = list(filter(None, path.split("/")))
    if len(path_list) == 0 or database is None:
        raise AttributeError("Empty path/DB")
    try:
        result = set_in_dict(database, path_list, value)
    except KeyError:
        raise KeyError("{} nested path must be created".format(path))
    except TypeError:
        raise TypeError("{} must delete existing path before extending it".format(path))
    return result

@app.route("/health")
def health():
    return "ok"

@app.route('/w/<path:subpath>', methods=['POST'])
def write(subpath):
    global DB_UPDATED
    p = escape(subpath)
    d = request.json
    try:
        v = d['value']
    except TypeError as E:
        app.logger.info(E)
        return jsonify({"Error": True, "msg": 'malformed post header/body request'}), 400
    lock.acquire()
    try:
        value = write_to_db(DB, p , v)
    except Exception as E:
        return jsonify({"Error": True, "msg": str(E)}), 400
    DB_UPDATED = True
    lock.notify_all()
    lock.release()
    return jsonify({"value": value, "path": escape(subpath)})

@app.route('/r/<path:subpath>')
def read(subpath):
    p = escape(subpath)
    d = request.json
    lock.acquire()
    value = read_from_db(DB, p)
    lock.notify_all()
    lock.release()
    return jsonify({"value": value, "path": p})


def thread_backup(sleep=10):
    global DB_UPDATED 
    global DB

    while True:
        time.sleep(10)
        if DB_UPDATED:
            lock.acquire()
            app.logger.info("Syncing DB to file")
            with open(BACKUP_FILE, 'w') as f:
                json.dump(DB, f)
            lock.notify_all()
            lock.release()
            DB_UPDATED = False

def read_db():
    global DB
    if not path.exists(BACKUP_FILE):
        return

    with open(BACKUP_FILE) as json_file:
        DB = json.load(json_file)

if __name__ == "__main__":
    read_db()
    b_t = threading.Thread(target=thread_backup, args=(1,))
    b_t.start()
    app.run(host= '0.0.0.0',threaded=True, port=9000, debug=True)