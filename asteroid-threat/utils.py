import requests
import datetime
import pandas as pd

API_KEY = ""

def get_todays_asteroids():
    today = datetime.date.today().isoformat()
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key={API_KEY}"
    res = requests.get(url).json()
    all_asteroids = []

    for date in res["near_earth_objects"]:
        for neo in res["near_earth_objects"][date]:
            try:
                diameter = neo["estimated_diameter"]["kilometers"]
                close_approach = neo["close_approach_data"][0]

                row = {
                    "name": neo["name"],
                    "min_diameter_km": diameter["estimated_diameter_min"],
                    "max_diameter_km": diameter["estimated_diameter_max"],
                    "velocity_kph": float(close_approach["relative_velocity"]["kilometers_per_hour"]),
                    "miss_distance_km": float(close_approach["miss_distance"]["kilometers"]),
                    "orbiting_body": close_approach["orbiting_body"]
                }
                all_asteroids.append(row)
            except:
                continue

    return pd.DataFrame(all_asteroids)