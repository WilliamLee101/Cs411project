import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
path_to_key = "/Users/williamlee/Desktop/CS411/Firebase/cs411-e12c0-firebase-adminsdk-z7icf-dbfcf166c2.json"
cred = credentials.Certificate(path_to_key)
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://cs411-e12c0-default-rtdb.firebaseio.com/"
})


#test cases
food = {}
food["burger"]=["100g", "5-star"]

#push and get
ref = db.reference("/")
# ref.set({"food":food})
print(ref.get("food"))

