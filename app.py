from flask import Flask, render_template, request, redirect, g, jsonify
import ticketpy
import json
import geopy.distance
from datetime import datetime
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

app = Flask(__name__)

tm_client = ticketpy.ApiClient('1m3jpoAZ65vufnoIEnQ47V5DjEoUGggG')



# This tells Flask to serve the static files from the 'static' folder
app.static_folder = 'static'


@app.route('/')
def auth():
    return render_template('auth.html')

@app.route('/index')
def index():
    return render_template('index.html')

# initialize a global variable for email and name
email = ""
name = ""

@app.route('/user/data', methods=['POST'])
def receive_email():
    global email
    global name
    
    # Assgin the info to the global variables of name and email
    email = request.json['email']
    name = request.json['name']

    print("email", email)
    print("Name:", name)
    return 'Email received!'

# initialize a global variable for longtitude and latitude
longitude = 0
latitude = 0

@app.route('/api/location', methods=['POST'])
def receive_location_data():
    global longitude
    global latitude
    data = request.get_json()
    
    # Assgin the info to the global variables of latitude and longitude
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # process the location data as needed
    
    print("latitude", latitude)
    print("longitude", longitude)

    response = {
        'status': 'location success'
    }
    return jsonify(response)

@app.route('/history')
def history():
    # Get the data from Firebase Realtime Database
    history_data = db.reference("history/"+name).get()
    print("history_data", history_data)

    # Render the history page with the data
    return render_template('history.html', history=history_data)


@app.route('/process-form', methods=['POST'])
def process_form():
    global email
    global latitude
    global longitude
    
    # get the input from frontend
    print("Processing form...")
    genre = request.form['genre']
    print("Genre:", genre)
    date_range = request.form['date_range']
    print("Date range:", date_range)
    max_price = request.form['max_price']
    print("Max price:", max_price)
    max_distance = request.form['max_distance']
    print("Max distance:", max_distance)
    state_code = request.form['state_code']
    print("State Code:", state_code)
    
    
    # process the input from the frontend
    
    start = date_range.split(" - ")[0] + "T00:00:00Z"
    finish = date_range.split(" - ")[1] + "T23:59:59Z"
    
    # use the ticketmaster api to find the events
    pages = tm_client.events.find(
    classification_name=genre,
    state_code= state_code,
    start_date_time=start,
    end_date_time=finish)
    
    event_list = []
    for page in pages:
        for event in page:
            event_dict = vars(event)
            event_list.append(event_dict)
            # print(event)

    
    # based on the input constraints (ptice and distance), return the valid events
    events_data = []
    for i in range(len(event_list)):
        coords_1 = (latitude, longitude)
        coords_2 = (float(event_list[i]["json"]["_embedded"]["venues"][0]["location"]["latitude"]), float(event_list[i]["json"]["_embedded"]["venues"][0]["location"]["longitude"]))
        if "price_ranges" not in event_list[i].keys() or event_list[i]["price_ranges"] == []:
            continue
        else:
            if float(max_price) >= float(event_list[i]["price_ranges"][0]["max"]) and float(max_distance) >= float(geopy.distance.geodesic(coords_1, coords_2).km):
                data = {}
                data["name"] = event_list[i]["name"]
                data["status"] = event_list[i]["status"]
                data["start_date"] = event_list[i]["local_start_date"]
                data["start_time"] = event_list[i]["local_start_time"]
                data["min_price"] = event_list[i]["price_ranges"][0]["min"]
                data["max_price"] = event_list[i]["price_ranges"][0]["max"]
                data["longitude"] = event_list[i]["json"]["_embedded"]["venues"][0]["location"]["longitude"]
                data["latitude"] = event_list[i]["json"]["_embedded"]["venues"][0]["location"]["latitude"]
                events_data.append(data)
        
    print(events_data)
    print("email", email)
    print("latitude2", latitude)
    print("longitude2", longitude)
    
    
    # get the current time
    now = datetime.now()

    current_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    #push to database
    ref = db.reference("/history")
    
    # we have to check if a user already exists in the database to prevent overwrite
    if str(name) in ref.get().keys():
        history = {}
        history[current_time]=events_data
        ref = db.reference("/history/"+str(name))
        ref.update(history)
    
    else:
        history = {}
        history[str(name)]={}
        history[str(name)][current_time] = events_data
        ref = db.reference("/history")
        
        print("keys", str(name), current_time)
        
        ref.update(history)


    return render_template('index.html', data=events_data)



if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)


