import streamlit as st
import pandas as pd
from utils import get_todays_asteroids
from live_prediction import predict_asteroids

st.set_page_config(page_title="Are We in Danger Today?", layout="wide")
st.title("🚀 Are We in Danger Today? 🌍")

st.markdown("""
    <style>
        body {
            background-color: #0b0c10;
            color: white;
        }

        .main {
            background-color: #0b0c10;
        }

        h1, h2, h3, h4 {
            color: #66fcf1 !important;
        }

        div[data-testid="stMarkdownContainer"] > div {
            font-family: 'Segoe UI', sans-serif;
        }

        .asteroid-card {
            background-color: #1f2833;
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 0 15px rgba(102, 252, 241, 0.2);
            transition: all 0.3s ease-in-out;
        }

        .asteroid-card:hover {
            box-shadow: 0 0 30px rgba(102, 252, 241, 0.6);
            transform: scale(1.02);
        }

        .hazardous {
            background-color: #660000 !important;
        }

        .safe {
            background-color: #003300 !important;
        }

        .stSelectbox > div {
            color: black;
        }

        .big-title {
            font-size: 36px;
            font-weight: bold;
            margin-top: 20px;
        }

        .sub-title {
            font-size: 22px;
            margin-bottom: 10px;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

api_key = ""  # replace with your actual key


df = get_todays_asteroids()

if df.empty:
    st.warning("No asteroid data available for today!")
else:
    df_preds, model, features = predict_asteroids(df)

    # Sort by distance and show top 10
    df_preds = df_preds.sort_values(by="miss_distance_km").head(10)

    st.markdown("### 🛰 Top 10 Nearest Asteroids Today")
    cols = st.columns(2)

    for i, row in df_preds.iterrows():
        with cols[i % 2]:
            is_danger = "🚨 HAZARDOUS" if row["hazardous_pred"] == 1 else "✅ Safe"
            danger_class = "hazardous" if row["hazardous_pred"] == 1 else "safe"

            with st.container():
                st.markdown(f"""
                <div class="asteroid-card {danger_class}">
                    <h4>{row['name']}</h4>
                    <ul>
                        <li>Speed: {row['velocity_kph']:.0f} kph</li>
                        <li>Distance: {row['miss_distance_km']:.0f} km</li>
                        <li>Status: <b>{is_danger}</b></li>
                    </ul>
                    <form action="#{row['name']}">
                        <input type="submit" value="View Details">
                    </form>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔎 Asteroid Details & Prediction Explanation")

    selected_name = st.selectbox("Choose an asteroid to inspect:", df_preds["name"].tolist())

    if selected_name:
        asteroid = df_preds[df_preds["name"] == selected_name].iloc[0]

        st.markdown(f"## 🪐 {asteroid['name']}")
        st.write(f"*Velocity:* {asteroid['velocity_kph']:.2f} kph")
        st.write(f"*Miss Distance:* {asteroid['miss_distance_km']:.2f} km")
        st.write(f"*Min Size:* {asteroid['min_diameter_km']:.4f} km")
        st.write(f"*Max Size:* {asteroid['max_diameter_km']:.4f} km")
        st.write(f"*Orbiting Body:* {asteroid['orbiting_body']}")
        st.write(f"*Prediction:* {'🚨 Hazardous' if asteroid['hazardous_pred'] == 1 else '✅ Not Hazardous'}")