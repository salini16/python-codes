import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import numpy as np
import datetime
import os

# ------------------------------------------------
# CONFIGURATION
# ------------------------------------------------
st.set_page_config(
    page_title="AirAware — Smart Air Quality System",
    page_icon="🌍",
    layout="wide",
)

# ------------------------------------------------
# CUSTOM DARK THEME
# ------------------------------------------------
st.markdown("""
    <style>
    body, .stApp {
        background-color: #1e1e1e;
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    .stButton button {
        background-color: #61dafb;
        color: #1e1e1e;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 16px;
    }
    .stButton button:hover {
        background-color: #4fa3d1;
        color: white;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# UTILITIES
# ------------------------------------------------
def get_aqi_color(aqi):
    """Return color and category for given AQI."""
    if aqi <= 50: return ('green', 'Good')
    elif aqi <= 100: return ('yellow', 'Satisfactory')
    elif aqi <= 200: return ('orange', 'Moderate')
    elif aqi <= 300: return ('red', 'Poor')
    else: return ('darkred', 'Severe')


# ------------------------------------------------
# NAVIGATION MENU
# ------------------------------------------------
menu = st.sidebar.radio(
    "🔍 Navigate",
    ["🏠 Home", "🏙️ City Live Data", "📅 Future Predictions", "ℹ️ About"],
    captions=["Dashboard overview", "Get city-wise AQI", "24H–10D forecasts", "Project info"]
)

# ------------------------------------------------
# 1️⃣ HOME PAGE
# ------------------------------------------------
if menu == "🏠 Home":
    st.title("🌍 AirAware: Air Quality Monitoring & Forecasting Dashboard")
    st.markdown("Welcome to **AirAware**, an AI-powered system for smarter, cleaner cities.")
    st.markdown("---")

    # File Upload Section
    st.subheader("📂 Upload Air Quality CSV Data")
    uploaded_file = st.file_uploader("Upload your .csv file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ File **{uploaded_file.name}** uploaded successfully!")
        st.dataframe(df.head(20), use_container_width=True)
    else:
        st.info("Upload a CSV file to view and analyze pollutant trends.")
        df = None

    # Mock AQI Value
    AQI_MOCK_VALUE = 82
    aqi_color, aqi_category = get_aqi_color(AQI_MOCK_VALUE)

    st.subheader("🌡️ Current Air Quality Index (AQI)")
    gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=AQI_MOCK_VALUE,
        title={'text': f"AQI: {aqi_category}", 'font': {'color': 'white', 'size': 24}},
        gauge={
            'axis': {'range': [0, 500]},
            'bar': {'color': '#4fa3d1'},
            'steps': [
                {'range': [0, 50], 'color': 'green'},
                {'range': [50, 100], 'color': 'yellow'},
                {'range': [100, 200], 'color': 'orange'},
                {'range': [200, 300], 'color': 'red'},
                {'range': [300, 500], 'color': 'purple'}
            ],
            'threshold': {'line': {'color': "white", 'width': 4}, 'value': AQI_MOCK_VALUE}
        }
    ))
    gauge.update_layout(paper_bgcolor="#2a2a2a", font={'color': 'white'}, height=350)
    st.plotly_chart(gauge, use_container_width=True)

    # Historical Mock Data
    st.subheader("📈 Pollutant Historical Trends")
    HISTORICAL_DATA = [
        {'pollutant': 'PM2.5', 'values': [55, 60, 65, 70, 75, 80, 70, 60, 50, 40], 'dates': pd.date_range("2025-10-01", periods=10)},
        {'pollutant': 'O3', 'values': [20, 25, 30, 35, 30, 25, 20, 15, 10, 5], 'dates': pd.date_range("2025-10-01", periods=10)},
        {'pollutant': 'NO2', 'values': [30, 32, 35, 40, 45, 42, 38, 35, 30, 25], 'dates': pd.date_range("2025-10-01", periods=10)},
    ]
    colors = {'PM2.5': '#ff7f0e', 'O3': '#2ca02c', 'NO2': '#d62728'}

    pollutant_fig = go.Figure()
    for item in HISTORICAL_DATA:
        pollutant_fig.add_trace(go.Scatter(
            x=item['dates'], y=item['values'], mode='lines+markers',
            name=item['pollutant'], line=dict(color=colors.get(item['pollutant'], '#61dafb'), width=2)
        ))
    pollutant_fig.update_layout(
        title="Pollutant Concentration Trends Over Time",
        xaxis_title="Date",
        yaxis_title="Concentration Level",
        plot_bgcolor="#3c4048",
        paper_bgcolor="#2a2a2a",
        font=dict(color="white"),
        height=400,
    )
    st.plotly_chart(pollutant_fig, use_container_width=True)

    # ------------------------------------------------
    # 📅 Calendar-based Prediction Section
    # ------------------------------------------------
    st.subheader("📅 Predict Pollutant Levels by Date")

    selected_date = st.date_input(
        "Select a date for prediction:",
        value=datetime.date.today() + datetime.timedelta(days=1),
        min_value=datetime.date.today(),
        max_value=datetime.date.today() + datetime.timedelta(days=10)
    )

    if st.button("🔮 Get Prediction for Selected Date"):
        st.info(f"Generating predicted pollutant levels for **{selected_date}**...")

        # Mock prediction data
        pollutants = ["PM2.5", "O3", "SO2", "NO2", "CO", "NH3"]
        levels = np.random.randint(30, 200, size=len(pollutants))
        units = ["µg/m³", "ppb", "ppb", "ppb", "ppm", "µg/m³"]

        pred_df = pd.DataFrame({"Pollutant": pollutants, "Predicted Level": levels, "Unit": units})
        pred_df["Color"] = [get_aqi_color(lv)[0] for lv in levels]

        # Bar Chart
        fig_pred = go.Figure(go.Bar(
            x=pred_df["Pollutant"],
            y=pred_df["Predicted Level"],
            marker_color=pred_df["Color"],
            text=[f"{lv} {u}" for lv, u in zip(pred_df["Predicted Level"], pred_df["Unit"])],
            textposition="outside"
        ))
        fig_pred.update_layout(
            title=f"Predicted Pollutant Levels on {selected_date}",
            xaxis_title="Pollutant",
            yaxis_title="Predicted Concentration",
            plot_bgcolor="#3c4048",
            paper_bgcolor="#2a2a2a",
            font=dict(color="white"),
            height=400,
        )
        st.plotly_chart(fig_pred, use_container_width=True)

    st.markdown("---")
    st.caption("💡 Built with Streamlit + Plotly | AirAware © 2025")

# ------------------------------------------------
# 2️⃣ CITY LIVE DATA (Corrected)
# ------------------------------------------------
elif menu == "🏙️ City Live Data":
    st.title("🏙️ City-wise Air Quality Data")

    # load from environment or user input
    api_key_env = os.getenv("AQICN_API_KEY", "")
    api_key = st.text_input("🔑 Enter your AQICN API Key", value=api_key_env, type="password")
    city = st.text_input("🌍 Enter City Name", "Hyderabad")

    if st.button("🌤️ Get Live AQI Data"):
        if not api_key:
            st.warning("Please enter your API key.")
        else:
            try:
                url = f"https://api.waqi.info/feed/{city}/?token={api_key}"
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    st.error(f"HTTP error from API: {response.status_code}")
                else:
                    data = response.json()
                    if data.get("status") != "ok" or "data" not in data:
                        st.error("API returned an error. Check your API key / city name.")
                    else:
                        aqi = data["data"].get("aqi", None)
                        dom_pol = data["data"].get("dominentpol", "Unknown").upper()
                        st.success(f"✅ AQI for **{city}**: {aqi} ({dom_pol})")

                        # Gauge
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=aqi if aqi is not None else 0,
                            title={'text': f"{city} — AQI"},
                            gauge={'axis': {'range': [0, 500]}, 'bar': {'color': '#4fa3d1'}}
                        ))
                        fig.update_layout(paper_bgcolor="#2a2a2a", font={'color': 'white'}, height=350)
                        st.plotly_chart(fig, use_container_width=True)

                        # Pollutant breakdown
                        pollutants = data["data"].get("iaqi", {})
                        if pollutants:
                            rows = []
                            for k, v in pollutants.items():
                                if isinstance(v, dict):
                                    val = v.get("v", None)
                                else:
                                    val = v
                                rows.append((k.upper(), val))
                            df_pol = pd.DataFrame(rows, columns=["Pollutant", "Value"]).sort_values("Pollutant").reset_index(drop=True)
                            st.dataframe(df_pol, use_container_width=True)
                        else:
                            st.info("No pollutant breakdown available.")
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")

# ------------------------------------------------
# 3️⃣ FUTURE PREDICTIONS
# ------------------------------------------------
elif menu == "📅 Future Predictions":
    st.title("📅 Future Air Quality Forecasts")

    forecast_type = st.selectbox(
        "Select forecast duration:",
        ["Next 24 Hours", "Next 5 Days", "Next 10 Days"]
    )

    if forecast_type == "Next 24 Hours":
        hours = 24
        freq = "H"
    elif forecast_type == "Next 5 Days":
        hours = 5 * 24
        freq = "H"
    else:
        hours = 10 * 24
        freq = "H"

    timestamps = pd.date_range(datetime.datetime.now(), periods=hours, freq=freq)
    predicted_aqi = np.random.randint(50, 250, size=hours)

    df = pd.DataFrame({"Time": timestamps, "Predicted AQI": predicted_aqi})
    fig = px.line(df, x="Time", y="Predicted AQI",
                  title=f"{forecast_type} Air Quality Forecast",
                  markers=True)
    fig.update_layout(
        plot_bgcolor="#3c4048",
        paper_bgcolor="#2a2a2a",
        font=dict(color="white"),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# 4️⃣ ABOUT
# ------------------------------------------------
elif menu == "ℹ️ About":
    st.title("ℹ️ About AirAware")
    st.markdown("""
    ### 🌍 AirAware: Smart Air Quality Monitoring & Prediction System
    **AirAware** combines AI + data science to predict pollution trends and visualize real-time data.

    **Features:**
    - Real-time AQI monitoring  
    - City-level pollution data (via API)  
    - 24-hour, 5-day & 10-day forecasting  
    - Calendar-based daily predictions  
    - CSV data upload & visualization  

    💡 Developed by: **Salini**  
    """)
