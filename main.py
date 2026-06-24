import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Egypt Transport AI",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_model_data():
    try:
        model_pkg = joblib.load('final_transport_model.pkl')
        try:
            df = pd.read_csv('Cleaned_Data_300_Rows.csv')
        except:
            df = pd.DataFrame({
                'delay_min': [10, 20, 30, 40],
                'pressure_index': [0.5, 1.2, 0.8, 1.5],
                'route_id': ['R1', 'R2', 'R3', 'R4'],
                'day_type': ['Weekday', 'Weekend', 'Weekday', 'Weekend'],
                'hour': [8, 12, 18, 22]
            })
        return model_pkg, df
    except Exception as e:
        st.error(f"Could not load 'final_transport_model.pkl'. Make sure it is in the same folder.")
        return None, None

model_data, df = load_model_data()

st.markdown("""
    <style>
    .success-box { padding:15px; background-color:#d4edda; border-left: 5px solid #155724; border-radius:5px; color:#155724; }
    .warning-box { padding:15px; background-color:#fff3cd; border-left: 5px solid #856404; border-radius:5px; color:#856404; }
    .danger-box { padding:15px; background-color:#f8d7da; border-left: 5px solid #721c24; border-radius:5px; color:#721c24; }
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

ROADS = {
    "Route 1: Western Desert (Edfu)": {"lat": 25.06440, "lon": 31.71639, "base_headway": 120},
    "Route 2: Qena-Luxor Agri":       {"lat": 25.70529, "lon": 31.19561, "base_headway": 300},
    "Route 3: Aswan East":            {"lat": 24.38443, "lon": 32.39179, "base_headway": 60},
    "Route 4: Marsa Alam Coast":      {"lat": 25.21230, "lon": 33.89343, "base_headway": 540}
}

def predict_delay(hour, passengers, weather_code, pressure, range_val):
    if model_data is None: return 0
    pipeline = model_data['pipeline']
    input_df = pd.DataFrame({
        'hour': [hour], 'passenger_count': [passengers],
        'weather_severity': [weather_code], 'pressure_index': [pressure],
        'delay_range': [range_val]
    })
    try:
        return max(0, pipeline.predict(input_df)[0])
    except:
        return 0

def get_status_html(minutes):
    if minutes < 15:
        return f'<div class="success-box">🟢 <b>Smooth Flow</b><br>Delay: {minutes:.0f} mins</div>'
    elif minutes < 45:
        return f'<div class="warning-box">🟡 <b>Moderate</b><br>Delay: {minutes:.0f} mins</div>'
    else:
        return f'<div class="danger-box">🔴 <b>Severe Traffic</b><br>Delay: {minutes:.0f} mins</div>'

st.sidebar.title("🚍 Egypt Transport AI")
portal = st.sidebar.radio("Select Interface:", ["👤 Commuter: Route Finder", "🏢 Company: Ops Center"])
st.sidebar.markdown("---")
st.sidebar.caption("Region: Upper Egypt & Red Sea")

if portal == "👤 Commuter: Route Finder":
    st.title("📍 Smart Route Selector")
    st.markdown("Compare delays across the **4 Main Arteries** to choose the fastest path.")
    with st.expander("📝 Trip Inputs", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            hour = st.slider("Departure Time (24h)", 0, 23, 9)
        with c2:
            passengers = st.slider("Current Bus Crowding", 0, 100, 40)
        with c3:
            weather = st.selectbox("Weather Condition", ["Sunny", "Cloudy", "Rainy"])
            weather_map = {"Sunny": 0, "Cloudy": 1, "Rainy": 2}
        traffic_txt = st.select_slider("General Traffic Report", options=["Light", "Moderate", "Heavy"])
        traffic_map = {"Light": 1, "Moderate": 2, "Heavy": 3}
    if st.button("🚀 Analyze Routes"):
        st.markdown("### 🚦 Live Status")
        cols = st.columns(4)
        best_route, min_delay = "", 999
        for i, (name, details) in enumerate(ROADS.items()):
            pressure = passengers / (details['base_headway'] + 1)
            pred = predict_delay(hour, passengers, weather_map[weather], pressure, traffic_map[traffic_txt])
            if pred < min_delay:
                min_delay, best_route = pred, name
            with cols[i]:
                st.markdown(f"#### {name}")
                st.caption(f"Freq: Every {details['base_headway']}m")
                st.markdown(get_status_html(pred), unsafe_allow_html=True)
        st.success(f"🏆 **Recommended Path:** {best_route} (Fastest Arrival)")
    st.markdown("### 🗺️ Network Coverage")
    map_data = pd.DataFrame.from_dict(ROADS, orient='index')
    st.map(map_data[['lat', 'lon']], zoom=6)

elif portal == "🏢 Company: Ops Center":
    st.title("📊 Operations Command Center")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Fleet Active", "142 Buses", "+5")
    k2.metric("Avg System Delay", f"{df['delay_min'].mean():.1f} min", "-12%")
    k3.metric("High Pressure Zones", "2", "R2, R4")
    k4.metric("Weather Alert", "None", "Sunny")
    st.divider()
    st.subheader("🛠️ What-If Simulation")
    c1, c2 = st.columns([1, 2])
    with c1:
        selected_route = st.selectbox("Select Route to Optimize", list(ROADS.keys()))
        base_h = ROADS[selected_route]['base_headway']
        st.write("---")
        new_h = st.slider(f"Adjust Headway (Current: {base_h}m)", 10, 600, base_h)
        st.caption("Lower headway = More buses = Less pressure")
    with c2:
        pax = 60
        old_p, new_p = pax / (base_h + 1), pax / (new_h + 1)
        d_old = predict_delay(18, pax, 0, old_p, 2)
        d_new = predict_delay(18, pax, 0, new_p, 2)
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.barh(["Current Schedule", "Optimized Schedule"], [d_old, d_new], color=['gray', 'green'])
        ax.set_xlabel("Expected Delay (Minutes)")
        st.pyplot(fig)
        if d_new < d_old:
            st.success(f"📉 **Projected Impact:** Delay reduced by {d_old - d_new:.1f} minutes per trip.")
        else:
            st.warning("Reducing headway further has diminishing returns.")
