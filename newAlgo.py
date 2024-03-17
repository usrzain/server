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
