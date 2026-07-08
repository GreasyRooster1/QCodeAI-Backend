import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth

load_dotenv()

cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "service-account.json")

if not firebase_admin._apps:
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Missing service account file at: {cred_path}")
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("Sucessfully connected to Firebase")