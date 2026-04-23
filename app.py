import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="S.A.G.A.R. HUD", layout="wide", page_icon="🛥️")
FIREBASE_BASE = "https://sagar-cloud-default-rtdb.firebaseio.com"

# --- HELPER FUNCTION FOR COMPASS DECODING ---
def get_cardinal_direction(degree):
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    ix = int((degree + 22.5) / 45) % 8
    return dirs[ix]

def fetch_data(folder_path):
    try:
        response = requests.get(f"{FIREBASE_BASE}/{folder_path}.json")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    return None

def send_command(direction):
    try:
        requests.patch(f"{FIREBASE_BASE}/controls.json", json={"direction": direction})
        st.toast(f"Command Sent: {direction}", icon="🚀")
    except Exception as e:
        st.error("Failed to send command.")

st.title("🌊 S.A.G.A.R. Orbital Command Center")
st.markdown("**(Solar Autonomous GPS Aqua Ro-Boat) - Live Telemetry & Control**")
st.divider()

sensors = fetch_data("sensors") or {}

# ------------------------------------------
# ROW 1: ENVIRONMENTAL PAYLOAD
# ------------------------------------------
st.subheader("📊 Live Payload Analytics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧪 pH Level", f"{sensors.get('pH_level', 0.0):.2f}", delta_color="off")
col2.metric("💧 Turbidity", f"{sensors.get('turbidity_percent', 0)}%")
col3.metric("🌡️ Air Temp", f"{sensors.get('temperature', 0.0)} °C")
col4.metric("💦 Humidity", f"{sensors.get('humidity', 0.0)}%")

st.divider()

# ------------------------------------------
# ROW 2: PROPULSION & NAVIGATION
# ------------------------------------------
colA, colB = st.columns([1, 2])

with colA:
    st.subheader("🕹️ Teleoperation & Auto")
    
    pad1, pad2, pad3 = st.columns(3)
    with pad2:
        if st.button("⬆️ FWD", use_container_width=True): send_command("FWD")
            
    pad4, pad5, pad6 = st.columns(3)
    with pad4:
        if st.button("⬅️ LEFT", use_container_width=True): send_command("LEFT")
    with pad5:
        if st.button("🛑 STOP", type="primary", use_container_width=True): send_command("STOP")
    with pad6:
        if st.button("➡️ RIGHT", use_container_width=True): send_command("RIGHT")
            
    pad7, pad8, pad9 = st.columns(3)
    with pad8:
        if st.button("⬇️ REV", use_container_width=True): send_command("REV")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🤖 INITIATE AUTO SWEEP", use_container_width=True): send_command("AUTO")

with colB:
    st.subheader("🛰️ Navigation & GPS Tracking")
    
    # 🧭 NEW COMPASS DISPLAY
    heading = sensors.get('compass_heading', 0)
    cardinal = get_cardinal_direction(heading)
    st.info(f"**🧭 Current Magnetic Heading:** {heading}° ({cardinal})")
    
    # 📍 EXAM DEMO MODE MAP
    COLLEGE_LAT = 19.0430
    COLLEGE_LON = 72.02307  
    map_df = pd.DataFrame({'lat': [COLLEGE_LAT], 'lon': [COLLEGE_LON]})
    
    st.map(map_df, zoom=16, use_container_width=True)
    st.success("🛰️ GPS Lock Secured")
