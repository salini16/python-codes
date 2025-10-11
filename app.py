import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Air Quality Monitoring & Forecasting",
    layout="wide",
    page_icon="🌍"
)

# Apply a custom dark theme
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
    </style>
""", unsafe_allow_html=True)


# -------------------- UTILITIES --------------------
def get_aqi_color(aqi):
    """Return AQI color and category"""
    if aqi <= 50: return ('green', 'Good')
    elif aqi <= 100: return ('yellow', 'Satisfactory')
    elif aqi <= 200: return ('orange', 'Moderate')
    elif aqi <= 300: return ('red', 'Poor')
    else: return ('darkred', 'Severe')


# -------------------- MOCK DATA --------------------
AQI_MOCK_VALUE = 78

HISTORICAL_DATA_MOCK = [
    {'pollutant': 'PM2.5', 'values': [55, 60, 65, 70, 75, 80, 70, 60, 50, 40], 'dates': pd.date_range("2025-10-01", periods=10)},
    {'pollutant': 'O3',    'values': [20, 25, 30, 35, 30, 25, 20, 15, 10, 5], 'dates': pd.date_range("2025-10-01", periods=10)},
    {'pollutant': 'NO2',   'values': [30, 32, 35, 40, 45, 42, 38, 35, 30, 25], 'dates': pd.date_range("2025-10-01", periods=10)},
]

PREDICTION_MOCK_DATA = [
    {'pollutant': 'PM2.5', 'level': 85, 'unit': 'µg/m³'},
    {'pollutant': 'O3', 'level': 32, 'unit': 'ppb'},
    {'pollutant': 'SO2', 'level': 15, 'unit': 'ppb'},
    {'pollutant': 'NO2', 'level': 45, 'unit': 'ppb'},
    {'pollutant': 'CO', 'level': 1.2, 'unit': 'ppm'},
    {'pollutant': 'NH3', 'level': 25, 'unit': 'µg/m³'},
]


# -------------------- HEADER --------------------
st.title("🌍 AirAware: Air Quality Monitoring & Forecasting Dashboard")
st.markdown("---")


# -------------------- FILE UPLOAD SECTION --------------------
st.subheader("📂 Upload Air Quality CSV Data")
uploaded_file = st.file_uploader("Upload your .csv file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ File **{uploaded_file.name}** uploaded successfully!")
    st.dataframe(df.head(20), use_container_width=True)
else:
    st.info("Upload a CSV file to view the preview.")
    df = None


# -------------------- AQI GAUGE CHART --------------------
st.subheader("🌡️ Current Air Quality Index (AQI)")

aqi_color, aqi_category = get_aqi_color(AQI_MOCK_VALUE)

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


# -------------------- POLLUTANT HISTORICAL TRENDS --------------------
st.subheader("📈 Pollutant Historical Trends")

colors = {'PM2.5': '#ff7f0e', 'O3': '#2ca02c', 'NO2': '#d62728'}

pollutant_fig = go.Figure()
for item in HISTORICAL_DATA_MOCK:
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


# -------------------- PREDICTION SECTION --------------------
st.subheader("📅 Forecasted Pollutant Levels")

selected_date = st.date_input(
    "Select date for prediction:",
    value=datetime.date.today() + datetime.timedelta(days=1)
)

if st.button("🔮 Get Predictions"):
    st.info(f"Generating predictions for **{selected_date}**...")

    pollutant_names = [p['pollutant'] for p in PREDICTION_MOCK_DATA]
    levels = [p['level'] for p in PREDICTION_MOCK_DATA]
    units = [p['unit'] for p in PREDICTION_MOCK_DATA]

    colors = [get_aqi_color(l * 1.5)[0] for l in levels]

    pred_fig = go.Figure(go.Bar(
        x=pollutant_names, y=levels, marker_color=colors,
        text=[f"{lvl} {unit}" for lvl, unit in zip(levels, units)],
        textposition="outside"
    ))
    pred_fig.update_layout(
        title=f"Predicted Pollutant Levels on {selected_date}",
        xaxis_title="Pollutant",
        yaxis_title="Predicted Concentration Level",
        plot_bgcolor="#3c4048",
        paper_bgcolor="#2a2a2a",
        font=dict(color="white"),
        height=400
    )
    st.plotly_chart(pred_fig, use_container_width=True)
else:
    st.info("Select a date and click **Get Predictions** to see the forecast.")


# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("💡 Built with Streamlit + Plotly | AirAware 2025 ©")

