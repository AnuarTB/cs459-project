import os
import firebase_admin

from flask import Flask
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask App
app = Flask(__name__)

# Initialize Firestore DB
if (not len(firebase_admin._apps)):
    cred = credentials.Certificate('/Users/thomasmattsson/Desktop/washing-machine-service-fdc63-firebase-adminsdk-la50h-eabce11589.json')
    default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

from washing_service import routes