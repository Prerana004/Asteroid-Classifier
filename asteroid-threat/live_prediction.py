import joblib

def predict_asteroids(df):
    model = joblib.load("asteroid_model.joblib")
    encoder = joblib.load("label_encoder.joblib")

    df["orbiting_body_enc"] = encoder.transform(df["orbiting_body"])

    features = df[["min_diameter_km", "max_diameter_km", "velocity_kph", "miss_distance_km", "orbiting_body_enc"]]
    df["hazardous_pred"] = model.predict(features)

    return df, model, features