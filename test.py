import random

# Charging station data
charging_stations = {
    'CS1': {'location': [24.9026626, 67.0765644], 'cost': 1.83, 'available_slots': 7, 'distance': 5.5},
    'CS2': {'location': [24.880088, 67.0522251], 'cost': 3.99, 'available_slots': 5, 'distance': 5.2},
    'CS3': {'location': [24.9024148, 67.0460271], 'cost': 2.2, 'available_slots': 8, 'distance': 5.5},
    'CS4': {'location': [24.9049357, 67.066777], 'cost': 2.76, 'available_slots': 2, 'distance': 2.6},
    'CS5': {'location': [24.8903276, 67.0856143], 'cost': 4.13, 'available_slots': 1, 'distance': 4.3},
}

# Constants
MAX_POPULATION_SIZE = min(10, len(charging_stations))  # Adjusted population size
MUTATION_RATE = 0.1
MAX_GENERATIONS = 100

# Function to calculate fitness based on maximum available slots, minimum distance, and minimum cost
def fitness(charging_station):
    max_available_slots = charging_stations[charging_station]['available_slots']
    distance = charging_stations[charging_station]['distance']
    cost = charging_stations[charging_station]['cost']

    # Define weights for each parameter (you can adjust these)
    max_available_slots_weight = 0.1  # Increased weight for slots
    min_distance_weight = 0.8
    min_cost_weight = 0.1

    # Calculate total fitness using weighted combination of parameters
    total_fitness = (max_available_slots_weight * max_available_slots +
                     min_distance_weight / distance +
                     min_cost_weight / cost)

    return total_fitness

# Genetic Algorithm functions
def initialize_population():
    return random.sample(list(charging_stations.keys()), MAX_POPULATION_SIZE)

def crossover(parent1, parent2):
    split_point = random.randint(1, len(parent1) - 1)
    child = parent1[:split_point] + parent2[split_point:]
    return child

def mutate(charging_station):
    return random.choice(list(charging_stations.keys()))

def select_parents(population):
    return random.choices(population, k=2)

def genetic_algorithm():
    population = initialize_population()

    for generation in range(MAX_GENERATIONS):
        parent1, parent2 = select_parents(population)
        child = crossover(parent1, parent2)
        if random.random() < MUTATION_RATE:
            child = mutate(child)
        population.append(child)

    # Select the best solution from the final population
    best_charging_station = max(population, key=fitness)

    return best_charging_station

# Main program
best_solution = genetic_algorithm()
print("Best Charging Station:", best_solution)
print("Fitness:", fitness(best_solution))
