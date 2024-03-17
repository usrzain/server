import firebase_admin
from firebase_admin import credentials, db
import time

# Initialize Firebase Admin SDK with the service account key JSON file
cred = credentials.Certificate("./accountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://evapp-a4979-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# Access the Firebase Realtime Database reference
ref = db.reference('/Locations')

# Function to handle changes in the database
def on_location_change(event):
    print('Change occurred in Location database')
    print(event.event_type)  # Can be 'put' or 'patch'
    print(event.data)  # Contains the data that was changed
#     # Handle the changes here as needed

# # Add a listener to the Location database
ref.listen(on_location_change)

# Function to add data to the Location database
def add_charging_stations(charging_stations):
    ref.set(charging_stations)
    print('added')

# Example charging stations data
charging_stations = {
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

# Add the charging stations to the Location database
add_charging_stations(charging_stations)

# Wait for changes (Ctrl+C to stop)
while True:
    time.sleep(1)  # Sleep to keep the program running and listen for changes
