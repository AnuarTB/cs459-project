from flask import request, jsonify
import requests

def get_statistics(wash_cycles):
    r = requests.get("http://www.statistics-service.com/calculate_daily_load", params={"wash_cycles":wash_cycles})
    return r

def test(wash_cycles):
    return wash_cycles