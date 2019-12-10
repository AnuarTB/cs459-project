from flask import request, jsonify
import requests


# Gets the status of a washing machine along with all timestamps that are newer than the timestamp in the parameter.
def get_wm_status(id, timestamp=None):
    if timestamp is not None:
        r = requests.get("http://www.washing_machine.com/<id>/fetch", params={"start_time":timestamp})
    else:
        r = requests.get("http://www.washing_machine.com/<id>/fetch")
    return r
