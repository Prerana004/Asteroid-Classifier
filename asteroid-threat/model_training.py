import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import requests


def fetch_historical_asteroids(pages=20, api_key="wvbCNYvCrXdgp3C7zWxJT9d8AGhlux0A4m2J0Aft"):
    all_data = []
    for i in range(pages):
        url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?page={i}&size=20&api_key={api_key}"
        res = requests.get(url).json()
        for neo in res["near_earth_objects"]:
            try:
                diameter = neo["estimated_diameter"]["kilometers"]
                close_approach = neo["close_approach_data"][0] if neo["close_approach_data"] else {}

                row = {
                    "name": neo["name"],
                    "hazardous": neo["is_potentially_hazardous_asteroid"],
                    "min_diameter_km": diameter["estimated_diameter_min"],
                    "max_diameter_km": diameter["estimated_diameter_max"],
                    "velocity_kph": float(close_approach.get("relative_velocity", {}).get("kilometers_per_hour", 0)),
                    "miss_distance_km": float(close_approach.get("miss_distance", {}).get("kilometers", 0)),
                    "orbiting_body": close_approach.get("orbiting_body", "UNKNOWN")
                }
                all_data.append(row)
            except:
                continue
    return pd.DataFrame(all_data)

df = fetch_historical_asteroids()
df.to_csv("asteroid_data.csv", index=False)

df.dropna(inplace=True)
le = LabelEncoder()
df["orbiting_body_enc"] = le.fit_transform(df["orbiting_body"])

X = df[["min_diameter_km", "max_diameter_km", "velocity_kph", "miss_distance_km", "orbiting_body_enc"]]
y = df["hazardous"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

print("Accuracy:", accuracy_score(y_test, clf.predict(X_test)))

# Save model
joblib.dump(clf, "asteroid_model.joblib")
joblib.dump(le, "label_encoder.joblib")