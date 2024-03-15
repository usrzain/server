from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import time
import threading
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Firebase Admin SDK with the service account key JSON file
cred = credentials.Certificate("./accountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://evapp-a4979-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# Access the Firebase Realtime Database reference
ref = db.reference('/Locations')

# Function to handle changes in the database
# def on_location_change(event):
#     print('Change occurred in Location database')
#     print(event.event_type)  # Can be 'put' or 'patch'
#     print(event.data)  # Contains the data that was changed
# #     # Handle the changes here as needed

# # # Add a listener to the Location database
# ref.listen(on_location_change)

# to make run firebase listening to run at a seprate thread
# Function to handle changes in the database




# Function to add data to the Location database
def add_charging_stations(charging_stations):
    ref.set(charging_stations)


# current Value

currSOC = 0.0
currLAT = 0.0
currLONG = 0.0
chargStation = 0
    




# Algo 
def find_best_charging_station(charging_stations, user_location, ev_range):
    def calculate_weighted_score(station):
        slots_weight = 0.5  # Adjust weights as needed
        distance_weight = 0.3
        cost_weight = 0.2

        distance = station["distance"]
        # Normalize distance to a 0-1 range (closer stations have higher scores)
        normalized_distance = 1 - (distance / max(station["distance"] for station in charging_stations.values()))

        # Penalty based on queue length, but only for stations with no slots
        penalty = -station["queue"] * (1 - station["available_slots"])

        score = station["available_slots"] * slots_weight + distance_weight * normalized_distance - cost_weight * station["cost"] + penalty
        return score

    def find_best_station():
        best_station_within_range = None
        best_score_within_range = float('-inf')

        closest_station_overall = None
        closest_distance = float('inf')

        for station_id, station in charging_stations.items():
            if station["distance"] <= ev_range:  # Check if within EV range
                score = calculate_weighted_score(station)
                if score > best_score_within_range:
                    best_station_within_range = station_id
                    best_score_within_range = score
            else:  # Station is outside EV range, but track closest one
                distance = station["distance"]
                if distance < closest_distance:
                    closest_station_overall = station_id
                    closest_distance = distance

        if best_station_within_range:
            return best_station_within_range  # Prioritize station within range
        else:
            return closest_station_overall  # If none within range, return closest overall

    # Find and return the best station
    best_station = find_best_station()

    if best_station:
        return charging_stations[best_station]
    else:
        return None

# Algo

# Dumy 
@app.route('/api/test', methods=['GET'])
def test():
  return jsonify('Hello')


# Error handling 
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404


@app.route('/api/extract_parameters', methods=['GET'])
def extract_parameters():
    print('request made ')
    if request.method == 'GET':
        current_soc = request.args.get('currentSOC')
        current_lat = request.args.get('currentLAT')  # Added for optional handling
        current_long = request.args.get('currentLONG')  # Added for optional handling

        currSOC = float(current_soc)
        currLAT = current_lat
        currLONG = current_long
            # Fetch the current data present in the "Locations" node
        data = ref.get()
        charging_stations = data
        print(charging_stations)
        apiKey = 'AIzaSyBeG5g3Ps44SleGRirPm4IcnC9BvwbLqDI'

        # This is just a dummy, actual data is fetched and stored in charging_stations
        # variable 
        charging_stations2 = {
            "CS1": {"location": [24.89627, 67.06616], "cost": 2.83, "available_slots": 2, "distance": 5.5,"queue": 0},
             "CS2": {"location": [24.89751, 67.07803], "cost": 2.87, "available_slots": 5, "distance": 5.2,"queue": 0},
            "CS3": {"location": [24.899, 67.07567], "cost": 2.9, "available_slots": 8, "distance": 5.5,"queue": 0},
            "CS4": {"location": [24.89629, 67.0697], "cost": 2.88, "available_slots": 0, "distance": 5.0,"queue": 4},
            "CS5": {"location": [24.89273, 67.08355], "cost": 2.89, "available_slots": 2, "distance": 5.3,"queue": 0},

            "CS6": {"location": [24.89704, 67.08431], "cost": 2.79, "available_slots": 2, "distance": 5.4,"queue": 0},
             "CS7": {"location": [24.89525, 67.09195], "cost": 2.91, "available_slots": 0, "distance": 4.4,"queue": 1},
            "CS8": {"location": [24.89094, 67.07656], "cost": 2.76, "available_slots": 0, "distance": 4.2,"queue": 2},
            "CS9": {"location": [24.88898, 67.08671], "cost": 2.88, "available_slots": 0, "distance": 4.3,"queue": 3},
            "CS10": {"location": [24.8944, 67.06461], "cost": 2.84, "available_slots": 2, "distance": 5.4,"queue": 0},
            "CS11": {"location": [24.88849, 67.06091], "cost": 2.75, "available_slots": 4, "distance": 4.3,"queue": 3},
            "CS12": {"location": [24.88992, 67.06816], "cost": 2.82, "available_slots": 1, "distance": 5.4,"queue": 0},
         }
        

        
        # Loop to update the distance field for each charging station
        for station_id, station_info in charging_stations.items():
               StationLat = station_info["location"][0]
               StationLong = station_info["location"][1]
               print(station_info["location"][0]); 
               apiurl = f'https://maps.googleapis.com/maps/api/distancematrix/json?departure_time=now&destinations={StationLat},{StationLong}&origins={currLAT},{currLONG}&key={apiKey}'
                   # Send the HTTP request to the Directions API
               response = requests.get(apiurl)

                   # Check if the request was successful
               if response.status_code == 200:
                     # Parse the JSON response
                   directions_data = response.json()
               
                   
                   distance_value = directions_data['rows'][0]['elements'][0]['distance']['value']
                   distance_value_in_km = distance_value / 1000 
                   station_info["distance"] = distance_value_in_km
               else:
                    print('error')
                  
             

                

              
        # print(charging_stations)  

        user_location = (currLAT, currLONG)
        max_Range = 50
        calculate_Range= currSOC/100*max_Range
        print(f' If Max Range is{ max_Range}then,Calculated Range is {calculate_Range}')
        # ev_range = float(input("Enter your EV's range in kilometers: "))

        best_station = find_best_charging_station(charging_stations, user_location, calculate_Range)
        if best_station:
            print("Best charging station within EV range based on your criteria:")
            print(f"- Station ID: {best_station}")
            print(f"- Slots: {best_station['available_slots']}")
            print(f"- Distance: {best_station['distance']} km")
            print(f"- Cost: ${best_station['cost']:.2f}")
            print(f"- Queue: {best_station['queue']}")
            if current_soc is not None:
                #  return jsonify({'success': True, 'currentSOC': current_soc, 'currentLAT': current_lat, 'currentLONG': current_long, 'CS':best_station}), 200
                 return jsonify({'CS':best_station}), 200
            else:
                return jsonify({'success': False, 'message': 'currentSOC parameter not found'}), 400
        else:
             print("No charging station found within your EV's range.")



# fetching the distance 
@app.route('/api/distanceandtime', methods=['GET']) 
def getIT():
    apiKey = 'AIzaSyCtDSgmH1koRCq9tU3zqf4T5tzsISG3nNY'
    if request.method == 'GET':
       
        current_lat = request.args.get('cLAT')  # Added for optional handling
        current_long = request.args.get('cLONG')
        dest_lat = request.args.get('dLAT')  # Added for optional handling
        dest_long = request.args.get('dLONG') 
        apiurl = f'https://maps.googleapis.com/maps/api/distancematrix/json?departure_time=now&destinations={dest_lat},{dest_long}&origins={current_lat},{current_long}&key={apiKey}'
                   # Send the HTTP request to the Directions API
        response = requests.get(apiurl)
        print(f'URL is this {apiurl} ')

                   # Check if the request was successful
        if response.status_code == 200:
                     # Parse the JSON response
            directions_data = response.json()                
            distance_value = directions_data['rows'][0]['elements'][0]['distance']['value']
            distance_value_in_km = distance_value / 1000 
            print(directions_data)
            return jsonify({'data': directions_data})

                   
        else:
            print('error')
            return jsonify({'data': 'directions_data'})
  

@app.route('/api/fetchPolylines', methods=['GET']) 
def poly():   
    apiKey = 'AIzaSyBeG5g3Ps44SleGRirPm4IcnC9BvwbLqDI'
    if request.method == 'GET':
        current_lat = request.args.get('cLAT')  # Added for optional handling
        current_long = request.args.get('cLONG')
        dest_lat = request.args.get('dLAT')  # Added for optional handling
        dest_long = request.args.get('dLONG') 


        apiurl = f'https://maps.googleapis.com/maps/api/directions/json?key={apiKey}&units=metric&origin={current_lat},{current_long}&destination={dest_lat},{dest_long}&mode=driving'
                   # Send the HTTP request to the Directions API
        response = requests.get(apiurl)
        print(f'URL is this {apiurl} ')

        if response.status_code == 200:
                     # Parse the JSON response
            polyLine_data = response.json()                
            
            print(polyLine_data)
            return jsonify(polyLine_data)

                   
        else:
            print('error')
            return jsonify({'data': 'ERROR'})
    

