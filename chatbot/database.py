import firebase_admin
from firebase_admin import credentials, db  # or from firebase_admin import db for Realtime Database
import json
# Initialize the Firebase Admin SDK
cred = credentials.Certificate("D:/SIH/SharkBYTE/chatbot/credentials.json")
firebase_admin.initialize_app(cred,{"databaseURL": "https://chtabot-805ef-default-rtdb.asia-southeast1.firebasedatabase.app/"})

# Initialize Firestore DB (or use db for Realtime Database)
ref=db.reference("/")
#db = firestore.client()
# Sample dataset
medicine_data = [
  {
    "medicine_name": "AmoxiCure",
    "type": "Antibiotic",
    "expiry_date": "2025-09-14",
    "manufacturing_date": "2023-09-14",
    "stock": "100",
    "last_updated_time": "2024-08-30T14:23:45Z"
  },
  {
    "medicine_name": "PainRelief",
    "type": "Analgesic",
    "expiry_date": "2024-12-02",
    "manufacturing_date": "2022-12-02",
    "stock": "70",
    "last_updated_time": "2024-08-30T10:15:22Z"
  },
  {
    "medicine_name": "CoughAway",
    "type": "Antitussive",
    "expiry_date": "2026-01-30",
    "manufacturing_date": "2024-01-30",
    "stock": "120",
    "last_updated_time": "2024-08-29T08:50:17Z"
  }
]

# Adding data to Firestore
def add_data():
    for medicine in medicine_data:
        # Each medicine is stored with its name as the document ID
        doc_ref = db.reference(f'medicines/{medicine["medicine_name"]}')
        doc_ref.set(medicine)

def get_data():
    # Fetching data from Firestore
        doc_ref = db.reference('medicines')
        medicines = doc_ref.get()
        return json.dumps(medicines, indent=4)
        
print(get_data())

    

