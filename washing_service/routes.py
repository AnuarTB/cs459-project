from flask import request, jsonify
from distutils.util import strtobool
from washing_service import app, db
from washing_service import statisticsServiceClient as stat_client
from washing_service import washingMachineClient as wm_client
import json, sys, datetime

user_ref = db.collection('users')
buildings_ref = db.collection('buildings')


@app.route('/users', methods=['GET'])
def read_users():

    try:
        # Check if ID was passed to URL query
        user_id = request.args.get('id')    
        if user_id:
            user = user_ref.document(user_id).get()
            return jsonify(user.to_dict()), 200
        else:
            all_users = [doc.to_dict() for doc in user_ref.stream()]
            return jsonify(all_users), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/buildings', methods=['GET'])
def read_buildings():
   
    try:
        # Check if ID was passed to URL query
        building_id = request.args.get('id')    
        if building_id:
            building = buildings_ref.document(building_id).get()
            return jsonify(building.to_dict()), 200
        else:
            all_buildings = [doc.to_dict() for doc in buildings_ref.stream()]
            return jsonify(all_buildings), 200
    except Exception as e:
        return f"An Error Occured: {e}"
        

@app.route('/buildings/<building_id>/<laundry_rooms>', methods=['GET'])
def read_rooms(building_id=None, laundry_rooms=None):

    building = buildings_ref.document(building_id)

    try:
        # Check if ID was passed to URL query
        laundry_room_id = request.args.get('id')    
        if laundry_room_id:
            room = building.collection(laundry_rooms).document(laundry_room_id).get()
            return jsonify(room.to_dict()), 200
        else:
            all_rooms = [doc.to_dict() for doc in building.collection(laundry_rooms).stream()]
            return jsonify(all_rooms), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/buildings/<building_id>/<laundry_room_id>/<washing_machines>', methods=['GET'])
def read_washing_machines(building_id=None, laundry_room_id=None, washing_machines=None):
    
    building = buildings_ref.document(building_id)
    room = building.collection('laundry_rooms').document(laundry_room_id)

    try:
        machine_id = request.args.get('id')
        if machine_id:
            machine = room.collection(washing_machines).document(machine_id).get()
            return jsonify(machine.to_dict()), 200
        else:
            all_machines = [doc.to_dict() for doc in room.collection(washing_machines).stream()]   
            return jsonify(all_machines), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/buildings/<building_id>/<laundry_room_id>/<washing_machine_id>/<wash_cycles>', methods=['GET'])
def read_wash_cycles(building_id=None, laundry_room_id=None, washing_machine_id=None, wash_cycles=None):

    building = buildings_ref.document(building_id)
    room = building.collection('laundry_rooms').document(laundry_room_id)
    machine = room.collection('washing_machines').document(washing_machine_id)

    try:
        wash_cycle_id = request.args.get('id')
        if wash_cycle_id:
            wash_cycle = machine.collection(wash_cycles).document(wash_cycle_id).get()
            return jsonify(wash_cycle.to_dict()), 200
        else:
            all_wash_cycles = [doc.to_dict() for doc in machine.collection(wash_cycles).stream()]
            return jsonify(all_wash_cycles), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/buildings/<building_id>/all_washing_machines', methods=['GET'])
def read_all_washing_machines(building_id=None, all_washing_machines=None):

    building = buildings_ref.document(building_id)
    try:          
        docs = building.collection('laundry_rooms').list_documents()
        machines_collections = []
        for doc in docs:
            machines_collections += doc.collections()

        wm_docs_list = []

        for col in machines_collections: 
            wm_docs_list += col.list_documents()

        all_washing_machines_snap = [doc.get() for doc in wm_docs_list]
        all_washing_machines = [doc.to_dict() for doc in all_washing_machines_snap]

        return jsonify(all_washing_machines), 200

    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/buildings/<building_id>/laundry_rooms/all_wash_cycles', methods=['GET'])
def read_all_wash_cycles(building_id=None, laundry_room_id=None) :

    building = buildings_ref.document(building_id)
    laundry_room_id = request.args.get('id')    

    try:
        if laundry_room_id:
            laundry_room_doc = building.collection('laundry_rooms').document(laundry_room_id)
            washing_machine_docs = laundry_room_doc.collection('washing_machines').list_documents()
            all_washing_machines_by_id_snap = []
            for doc in washing_machine_docs:
                    temp_wash_cycle_docs = doc.collection('wash_cycles').list_documents()
                    all_washing_machines_by_id_snap += [doc.get() for doc in temp_wash_cycle_docs]

            all_wash_cycles = [doc.to_dict() for doc in all_washing_machines_by_id_snap]

            return jsonify(all_wash_cycles), 200        
        else:
            all_laundry_room_docs = building.collection('laundry_rooms').list_documents()
            all_washing_machines_snap = []
            
            for doc in all_laundry_room_docs:
                temp_washing_machine_docs = doc.collection('washing_machines').list_documents()
                for doc in temp_washing_machine_docs:
                    temp_wash_cycle_docs = doc.collection('wash_cycles').list_documents()
                    all_washing_machines_snap += [doc.get() for doc in temp_wash_cycle_docs]

            all_wash_cycles = [doc.to_dict() for doc in all_washing_machines_snap]

            return jsonify(all_wash_cycles)

    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/buildings/<building_id>/<laundry_room_id>/get_daily_stat', methods=['GET'])
def invoke_stat_service(building_id=None, laundry_room_id=None):
    (wash_cycles, num_of_machines) = read_all_wash_cycles_json(building_id, laundry_room_id)
    
    weekday = request.args.get('weekday')    

    if weekday:
        stats = stat_client.get_statistics(wash_cycles, num_of_machines, weekday)
    else:
        stats = stat_client.get_statistics_today(wash_cycles, num_of_machines)
    
    return jsonify(stats)


@app.route('/buildings/<building_id>/<laundry_room_id>/<washing_machine_id>/update', methods=['GET'])
def update_washing_machine(building_id=None, laundry_room_id=None, washing_machine_id=None):
    is_running = request.args.get('is_running')
    building = buildings_ref.document(building_id)
    room = building.collection('laundry_rooms').document(laundry_room_id)
    machine = room.collection('washing_machines').document(washing_machine_id)

    try:
        if is_running:
            machine.update({"is_running": bool(strtobool(is_running))})
        
            return jsonify({"success": True}), 200
        else:
            is_running = wm_client.get_wm_status(washing_machine_id)
            machine.update({"is_running": bool(strtobool(is_running))})
            
            return jsonify({"success": True}), 200

    except Exception as e:
        return f"An Error Occured: {e}" 


def read_all_wash_cycles_json(building_id=None, laundry_room_id=None):
    
    building = buildings_ref.document(building_id)
                
    laundry_room_doc = building.collection('laundry_rooms').document(laundry_room_id)
    washing_machine_docs = laundry_room_doc.collection('washing_machines').list_documents()

    # Count number of machines.
    all_machines = [doc.to_dict() for doc in laundry_room_doc.collection('washing_machines').stream()]   
    num_of_machines = len(all_machines)

    all_washing_machines_by_id_snap = []
    for doc in washing_machine_docs:
        temp_wash_cycle_docs = doc.collection('wash_cycles').list_documents()
        all_washing_machines_by_id_snap += [doc.get() for doc in temp_wash_cycle_docs]
        
        all_wash_cycles = [doc.to_dict() for doc in all_washing_machines_by_id_snap]

    data = json.dumps(all_wash_cycles, default=convert_timestamp)

    return data, num_of_machines

    
def convert_timestamp(item_date_object):
    if isinstance(item_date_object, (datetime.date, datetime.datetime)):
        return item_date_object.timestamp()


# @app.route('/add', methods=['POST'])
# def create():
#     """
#         create() : Add document to Firestore collection with request body
#         Ensure you pass a custom ID as part of json body in post request
#         e.g. json={'id': '1', 'title': 'Write a blog post'}
#     """
#     try:
#         id = request.json['id']
#         user_ref.document(id).set(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

# @app.route('/buildings/<building_id>/<laundry_room_id>/<washing_machine_id>/<wash_cycles>', methods=['POST', 'PUT'])
# def update():
#     """
#         update() : Update document in Firestore collection with request body
#         Ensure you pass a custom ID as part of json body in post request
#         e.g. json={'id': '1', 'title': 'Write a blog post today'}
#     """
#     try:
#         id = request.json['id']
#         user_ref.document(id).update(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

# @app.route('/delete', methods=['GET', 'DELETE'])
# def delete():
#     """
#         delete() : Delete a document from Firestore collection
#     """
#     try:
#         # Check for ID in URL query
#         todo_id = request.args.get('id')
#         user_ref.document(todo_id).delete()
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

