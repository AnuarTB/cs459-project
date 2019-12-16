from flask import request, jsonify
import requests


def get_statistics(wash_cycles, num_of_machines):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    payload = {'wach_cycles': wash_cycles, 'num_of_machines': str(num_of_machines)}

    r = requests.get("http://localhost:5002/get_stat", json=payload, headers=headers)
    data = r.json()
    return data

def test(wash_cycles):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    r = requests.get("http://localhost:5002", headers=headers)
    return r.content
