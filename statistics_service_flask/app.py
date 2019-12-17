from flask import Flask, jsonify
from flask_restful import Resource, Api, request
import sys, json, datetime
from datetime import date, datetime

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class StatisticsToday(Resource):
    def get(self):
        payload = request.get_json()
        num_of_machines = json.loads(payload['num_of_machines'])
        wash_cycles = json.loads(payload['wach_cycles'])
        today_list = []

        for cycle in wash_cycles:
            if is_day(cycle['start_time']) or is_day(cycle['end_time']):
                today_list.append(cycle)

        load_list = calc_load(today_list, num_of_machines)

        return load_list

class StatisticsWeekday(Resource):
    def get(self):
        payload = request.get_json()
        num_of_machines = json.loads(payload['num_of_machines'])
        wash_cycles = json.loads(payload['wach_cycles'])
        weekday = int(json.loads(payload['week_day']))
        today_list = []

        for cycle in wash_cycles:
            if is_day(cycle['start_time'], weekday) or is_day(cycle['end_time'], weekday):
                today_list.append(cycle)

        load_list = calc_load(today_list, num_of_machines)

        return load_list


def is_day(unix_timestamp, weekday=None):
    if weekday:
        return weekday == datetime.utcfromtimestamp(unix_timestamp).weekday()
    else:
        now = datetime.now()
        return now.weekday() == datetime.utcfromtimestamp(unix_timestamp).weekday()


def calc_load(today_list, num_of_machines):
    load_list = [None] * 6
    minute_list = [0] * 1440

    # Populate minutelist with active minutes
    for cycle in today_list:
        temp_start_min = (datetime.utcfromtimestamp(cycle['start_time']).hour)*60
        + (datetime.utcfromtimestamp(cycle['start_time']).minute)
        temp_end_min = (datetime.utcfromtimestamp(cycle['end_time']).hour)*60
        + (datetime.utcfromtimestamp(cycle['end_time']).minute)

        for i in range(temp_start_min, temp_end_min):
            minute_list[i] += 1

    # Calcualte load and put in load list
    for i in range(6):
        load_list[i] = (sum_part_list(minute_list, (240 * i), (240 * (i+1)))
        / 240) / num_of_machines

    return load_list


def sum_part_list(list, start, stop):
    sum = 0
    for i in range (start, stop):
        sum += list[i]
    return sum


api.add_resource(HelloWorld, '/')
api.add_resource(StatisticsToday, '/get_stat')
api.add_resource(StatisticsWeekday, '/get_stat_weekday')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
