from flask import request, jsonify
from washing_service import app, db
import requests


def get_wm_status(timestamp):
    r = requests.get("http://www.washing_machine.com/fetch", params={"start_time":timestamp})
    return r

