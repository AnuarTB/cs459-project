from flask import request, jsonify
import requests

# Returns average the load percentage for the weekday at time of calling. 
# Returns load over six 4-hour blocks like this: [load, load, load, load, load, load]
def get_statistics_today(wash_cycles, num_of_machines):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    payload = {'wach_cycles': wash_cycles, 'num_of_machines': str(num_of_machines)}

    r = requests.get("http://localhost:5001/get_stat", json=payload, headers=headers)
    data = r.json()
    return data

# Returns average the load percentage for a given weekday. Weekday given as integer with Mon = 0 amd Sun = 6. 
# Returns load over six 4-hour blocks like this: [load, load, load, load, load, load]
def get_statistics(wash_cycles, num_of_machines, weekday):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    payload = {'wach_cycles': wash_cycles, 'num_of_machines': str(num_of_machines), "week_day": str(weekday)}

    r = requests.get("http://localhost:5001/get_stat_weekday", json=payload, headers=headers)
    data = r.json()
    return data
