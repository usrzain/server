from flask import Flask, jsonify, request
import requests
import folium

app = Flask(__name__)

def find_petrol_pumps_nearby(latitude, longitude, radius):
    api_key = "AIzaSyBeG5g3Ps44SleGRirPm4IcnC9BvwbLqDI"  # Replace this with your actual Google Places API key
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type=gas_station&key={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    petrol_pumps = {'east': [], 'west': [], 'north': [], 'south': []}
    if 'results' in data:
        for result in data['results']:
            name = result['name']
            location = result['geometry']['location']
            distance = get_distance_from_current_location(latitude, longitude, location['lat'], location['lng'])
            if distance is not None:
                direction = get_direction_from_current_location(latitude, longitude, location['lat'], location['lng'])
                petrol_pumps[direction].append({'name': name, 'location': location, 'distance': distance})
    else:
        print("Error fetching petrol pumps:", data.get('error_message', 'Unknown error'))
    
    return petrol_pumps

def get_distance_from_current_location(current_lat, current_lng, dest_lat, dest_lng):
    api_key = "AIzaSyBeG5g3Ps44SleGRirPm4IcnC9BvwbLqDI"  # Replace this with your actual Google Maps API key
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={current_lat},{current_lng}&destinations={dest_lat},{dest_lng}&key={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    if 'rows' in data and len(data['rows']) > 0:
        row = data['rows'][0]
        if 'elements' in row and len(row['elements']) > 0:
            element = row['elements'][0]
            if 'distance' in element:
                return element['distance']['value']  # Distance in meters
    return None

def get_direction_from_current_location(current_lat, current_lng, dest_lat, dest_lng):
    if dest_lat > current_lat:
        return 'north'
    elif dest_lat < current_lat:
        return 'south'
    elif dest_lng > current_lng:
        return 'east'
    else:
        return 'west'

# API endpoint to find petrol pumps within the specified radius and their distances from current location
@app.route('/api/petrol_pumps', methods=['GET'])
def get_petrol_pumps_nearby():
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        radius = int(request.args.get('radius', 10000))  # Default radius is 10000 meters (10 km)
    except ValueError:
        return jsonify({'message': 'Invalid latitude, longitude, or radius provided.'}), 400
    
    petrol_pumps = find_petrol_pumps_nearby(latitude, longitude, radius)
    
    if petrol_pumps:
        # Prepare response data
        response_data = {}
        for direction, pumps in petrol_pumps.items():
            response_data[direction] = pumps
        
        return jsonify(response_data)
    else:
        return jsonify({'message': 'No petrol pumps found within the specified radius.'})

if __name__ == '__main__':
    app.run(debug=True)
