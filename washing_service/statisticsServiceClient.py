from flask import request, jsonify
import requests

def get_statistics(wash_cycles):
    r = requests.get("http://www.statistics-service.com/calculate_daily_load", params={"wash_cycles":wash_cycles})
    return r

def test(wash_cycles):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    r = requests.get("http://localhost:5001", headers=headers)
    return r.content