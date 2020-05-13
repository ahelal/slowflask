#!/usr/bin/env python3
from flask import Flask
from flask import jsonify
from flask import request
import os
from datetime import datetime
# import datetime
import db

app = Flask(__name__)

DB_CONNECTION_STATUS = False

def f(x):
    start_time = datetime.now()
    while True:
        x*x
        time_delta = datetime.now() - start_time
        if time_delta.total_seconds() >= 1:
            break

def slow():
    r = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    f(r)

def valid_date(str_time):
    day,month,year = str_time.split('/')
    isValidDate = True
    try :
        datetime.datetime(int(year),int(month),int(day))
        return True
    except ValueError :
        return False

def locations():
    try:
        v = db.db_read("location")
    except Exception as E:
        return []

def is_location(l):
    return l in locations

@app.route("/")
def root():
    slow()
    return "Welcome!"

@app.route("/health")
def health():
    db_status = db.db_ping()
    return jsonify({"API": True, "DB": db_status})

@app.route("/list_items")
def list_product():
    try:
        v = db.db_read("item_definition")
    except Exception as E:
        return str(E), 500
    return v

@app.route("/list_location")
def list_location():
    if locations != []:
        return locations
    return "No locations defined ", 500

@app.route("/list_pickups")
def list_pickups():
    try:
        v = db.db_read("transactions")
    except Exception as E:
        return str(E), 500
    return v

@app.route('/transaction', methods=['POST'])
def write():
    d = request.json
    try:
        name = d.get("name").strip()
        date = d.get("date").strip()
        location = d.get("location").strip()
        items = d.get("items")
    except Exception as E:
        return str(E), 402
    
    if len(name) == 0:
        return "name is required", 402
    
    if not valid_date(date):
        return "date is required and must be valid", 402
    if len(location) == 0 or not is_location(l):
        return "location is required and must be defined", 402
    
    last_transaction_id = db.db_read("last_transaction_id")
    data = {last_transaction_id +1 : {
        "name": name,
        "date": date,
        "location": location,
        "items": items
    } }
    return db.db_write("transactions". data)
    
if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=8080)
