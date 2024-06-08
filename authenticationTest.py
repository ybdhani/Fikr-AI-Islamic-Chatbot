import firebase_admin
from firebase_admin import credentials, firestore
import json

# Path to your service account key JSON file
service_account_key_path = 'logintest-12b8b-e89e95a21c52.json'

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Function to upload JSON data to Firestore
def upload_json_to_firestore(json_file_path, collection_name):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            
            if isinstance(data, dict):
                # Ensure we handle a single dictionary
                session_id = data.get('session_id')
                if session_id:
                    db.collection(collection_name).document(session_id).set(data)
                    print(f'Data uploaded for session ID: {session_id}')
                else:
                    print('Session ID is missing in the entry.')
            elif isinstance(data, list):
                for entry in data:
                    session_id = entry.get('session_id')
                    if session_id:
                        db.collection(collection_name).document(session_id).set(entry)
                        print(f'Data uploaded for session ID: {session_id}')
                    else:
                        print('Session ID is missing in one of the entries.')
            else:
                print('JSON data is not a dictionary or list of dictionaries')
    except Exception as e:
        print(f'Error uploading data: {e}')

# Specify the JSON file path and collection name
json_file_path = 'chat_history.json'
collection_name = 'sessions'

# Call the function to upload JSON data
upload_json_to_firestore(json_file_path, collection_name)
