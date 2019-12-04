from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'



config = {
  "apiKey": os.environ['AIzaSyBuIgw9ioawAlgSln9IW4QKnKJYPdy3TEc'],
  "authDomain": "washing-machine-service-fdc63.firebaseapp.com",
  "databaseURL": "https://washing-machine-service-fdc63.firebaseio.com",
  "projectId": "washing-machine-service-fdc63",
  "storageBucket": "washing-machine-service-fdc63.appspot.com",
  "serviceAccount": "washing-machine-service-fdc63-firebase-adminsdk-la50h-eabce11589.json",
  "messagingSenderId": "703001830397"
}