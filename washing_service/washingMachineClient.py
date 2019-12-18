from flask import request, jsonify
import requests


# Gets the status of a washing machine along with all timestamps that are newer than the timestamp in the parameter.
def get_wm_status(id, timestamp=None):
    if timestamp is not None:
        r = requests.get("http://192.168.43.91:1880/check", params={"start_time":timestamp})
        data = r.json()
    else:
        r = requests.get("http://192.168.43.91:1880/check")
        data = r.json()
    return data

