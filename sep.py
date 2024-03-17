# import folium
import random
# import itertools

# Constants
DISCHARGING_RATE = 0.5  # Example discharging rate in km per minute

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5

# Function to calculate the remaining range of an EV
def calculate_remaining_range(battery_status):
    return battery_status / DISCHARGING_RATE

# Function to initialize charging stations and user's EV with fixed values within a circular radius
def initialize_locations(user_location):
    charging_stations = {}
    
    # Fixed user's battery status
    user_battery_status = 25  # Replace with your desired initial battery status

    remaining_range = calculate_remaining_range(user_battery_status)

    # Fixed charging station locations
    charging_stations = {
        'CS1': {'location': [24.9601644, 66.8384994], 'cost': 1.83, 'available_slots': 7},
        'CS2': {'location': [24.8962234, 66.9905484], 'cost': 3.99, 'available_slots': 5},
        'CS3': {'location': [24.8992013, 67.0959056], 'cost': 2.2, 'available_slots': 8},
        'CS4': {'location': [24.8828, 67.0777], 'cost': 2.76, 'available_slots': 2},
        'CS5': {'location': [24.8828, 67.0777], 'cost': 4.13, 'available_slots': 1},
        'CS6': {'location': [24.8456, 67.0365], 'cost': 1.89, 'available_slots': 7},
        # 'CS7': {'location': [-16.64825187095856, 61.85348557252851], 'cost': 2.03, 'available_slots': 2},
        # 'CS8': {'location': [-85.83757555814721, 21.27866235998792], 'cost': 2.79, 'available_slots': 6},
        # 'CS9': {'location': [-12.520203875102766, 177.40933188483928], 'cost': 4.71, 'available_slots': 7},
        # 'CS10': {'location': [58.23955537545331, -103.2763748025472], 'cost': 1.9, 'available_slots': 7}
    }

    # Calculate distance between the user and each charging station
    for cs, properties in charging_stations.items():
        properties['distance'] = calculate_distance(user_location, properties['location'])

    return user_location, user_battery_status, remaining_range, charging_stations

# Function to calculate fitness based on maximum available slots, minimum distance, and minimum cost
def fitness(charging_station, charging_stations):
    max_available_slots = charging_stations[charging_station]['available_slots']
    distance = charging_stations[charging_station]['distance']
    cost = charging_stations[charging_station]['cost']

    # Define weights for each parameter (you can adjust these)
    max_available_slots_weight = 0.4
    min_distance_weight = 0.5  # Increased weight for distance
    min_cost_weight = 0.1  # Decreased weight for cost

    # Calculate total fitness using weighted combination of parameters
    total_fitness = -(max_available_slots_weight * max_available_slots +
                      min_distance_weight * distance +
                      min_cost_weight * cost)

    return total_fitness

# Genetic Algorithm functions
def initialize_population(charging_stations):
    return list(charging_stations.keys())

def crossover(parent1, parent2):
    split_point = random.randint(1, len(parent1) - 1)
    child = parent1[:split_point] + parent2[split_point:]
    return child

def mutate(charging_station):
    return random.choice(list(charging_stations.keys()))

def select_parents(population):
    return random.sample(population, 2)

def genetic_algorithm(charging_stations):
    population = initialize_population(charging_stations)

    for generation in range(100):
        parent1, parent2 = select_parents(population)
        child = crossover(parent1, parent2)
        if random.random() < 0.1:  # 10% chance of mutation
            child = mutate(child)
        population.append(child)

    # Select the best solution from the final population
    best_charging_station = max(population, key=lambda x: fitness(x, charging_stations))

    # printing the best charging station
    print("\nBest Charging Station:", best_charging_station)
    return best_charging_station

# Visualize the charging stations and user's EV with the highlighted path
# def visualize_map(user_location, user_battery_status, remaining_range, charging_stations, best_solution):
#     # Create a folium map centered at the user's location
#     map_center = [user_location[0], user_location[1]]
#     my_map = folium.Map(location=map_center, zoom_start=12)

#     # Add user's EV marker to the map with remaining range information
#     popup_text_user = f"User's EV<br>Remaining Battery: {user_battery_status}%<br>Remaining Range: {remaining_range:.2f} km"
#     folium.Marker(location=user_location, popup=popup_text_user, icon=folium.Icon(color='blue')).add_to(my_map)

#     # Add charging station markers with popup information
#     for cs, properties in charging_stations.items():
#         popup_text = f"{cs}<br>Cost: {properties['cost']}<br>Distance: {properties['distance']}<br>Availability: {properties['available_slots']} Slots"
#         folium.Marker(location=properties['location'], popup=popup_text, icon=folium.Icon(color='red')).add_to(my_map)

#     # Add edge between user's EV and the best charging station
#     best_cs_location = charging_stations[best_solution]['location']
#     folium.PolyLine(locations=[user_location, best_cs_location], color="green").add_to(my_map)

#     # Save the map as an HTML file
#     my_map.save("charging_station_assignment_map.html")

#     print("Interactive map saved as charging_station_assignment_map.html")

# Main program
# Input the user's location
user_location_input = input("Enter the user's location (latitude, longitude) separated by a comma (e.g., 30, 40): ")
user_location = [float(coord) for coord in user_location_input.split(",")]

user_location, user_battery_status, remaining_range, charging_stations = initialize_locations(user_location)

print("User's EV Location:", user_location)
print("User's Battery Status:", user_battery_status)
print("Remaining Range:", remaining_range)

print("Charging Stations:")
for cs, properties in charging_stations.items():
    print(f"{cs}: Location - {properties['location']}, Cost - {properties['cost']}, Distance - {properties['distance']}, "
          f"Availability - {properties['available_slots']} Slots")

genetic_algorithm(charging_stations)


# Visualize the best charging station and user's EV with the highlighted path
# visualize_map(user_location, user_battery_status, remaining_range, charging_stations, best_charging_station)
