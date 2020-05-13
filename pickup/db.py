import os
import requests
DB_HOST = os.getenv("DB_HOS>T", "http://localhost:9000")


def db_ping():
    try:
        r = requests.get(DB_HOST + "/health", timeout=1)
    except Exception as E:
        print("Error pinging DB", E)
        return False
    return True

def db_read(p):
    url = "{}/r/{}".format(DB_HOST,p)
    r = requests.get(url, timeout=2)
    data = r.json()
    if data.get("value", None):
        return data
    else:
        return {"value": None}


def db_write(p, d):
    url = "{}/w/{}".format(DB_HOST,p)
    data = {"value": d}
    try:
        r = requests.get(url,json=data, timeout=2)
        return True
    except Exception as E:
        return False
