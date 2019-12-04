from flask import request, jsonify
from washing_service import app, db


user_ref = db.collection('users')
buildings_ref = db.collection('buildings')

@app.route('/users', methods=['GET'])
def read_users():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
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
    """
        read() : Fetches documents from Firestore collection as JSON
        building : Return document that matches query ID
        all_buildings : Return all documents
    """
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

# @app.route('/update', methods=['POST', 'PUT'])
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