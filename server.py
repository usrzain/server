from flask import Flask, jsonify, request
import requests
import folium

app = Flask(__name__)

def find_petrol_pumps_nearby(latitude, longitude, radius=5000):
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

# API endpoint to find petrol pumps within 5 km radius and their distances from current location
@app.route('/api/petrol_pumps', methods=['GET'])
def get_petrol_pumps_nearby():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    
    petrol_pumps = find_petrol_pumps_nearby(latitude, longitude, radius=5000)
    
    if petrol_pumps:
        # Create a folium map centered at the current location
        my_map = folium.Map(location=[latitude, longitude], zoom_start=12)
        
        # Add markers for petrol pumps
        colors = {'east': 'red', 'west': 'blue', 'north': 'green', 'south': 'purple'}
        for direction, pumps in petrol_pumps.items():
            for pump in pumps:
                folium.Marker(location=[pump['location']['lat'], pump['location']['lng']], popup=pump['name'], icon=folium.Icon(color=colors[direction])).add_to(my_map)
        
        # Save the map as an HTML file
        map_file = "petrol_pumps_map.html"
        my_map.save(map_file)
        
        return f'<p>Map generated with petrol pumps highlighted. <a href="{map_file}" target="_blank">View Map</a></p>'
    else:
        return jsonify({'message': 'No petrol pumps found within 5 km radius.'})

if __name__ == '__main__':
    app.run(debug=True)
