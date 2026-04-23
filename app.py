import streamlit as st
import requests
import pandas as pd

# ==========================================
# ⚙️ SYSTEM CONFIGURATION
# ==========================================
st.set_page_config(page_title="S.A.G.A.R. HUD", layout="wide", page_icon="🛥️")
FIREBASE_BASE = "https://sagar-cloud-default-rtdb.firebaseio.com"

# ==========================================
# 📡 CLOUD COMMUNICATION FUNCTIONS
# ==========================================
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

# ==========================================
# 🚀 TACTICAL HUD LAYOUT
# ==========================================
st.title("🌊 S.A.G.A.R. Orbital Command Center")
st.markdown("**(Solar Autonomous GPS Aqua Ro-Boat) - Live Telemetry & Control**")

# Fetch all sensor data first so we can check for emergencies
sensors = fetch_data("sensors") or {}

# --- 🚨 NEW FEATURE: ACTIVE COLLISION WARNING BANNER ---
obstacle_detected = sensors.get("obstacle_warning", False)
sonar_dist = sensors.get("sonar_distance", 0)

if obstacle_detected:
    st.error(f"🚨 **COLLISION AVOIDANCE TRIGGERED!** Obstacle detected at {sonar_dist} cm. Autopilot disengaged and motors locked.")
else:
    # If the distance is 999, it means the radar sees nothing in front of it.
    display_dist = "Clear" if sonar_dist == 999 else f"{sonar_dist} cm"
    st.success(f"🟢 Radar Clear. Forward vector safe. (Nearest object: {display_dist})")

st.divider()

# ------------------------------------------
# ROW 1: ENVIRONMENTAL PAYLOAD (SENSORS)
# ------------------------------------------
st.subheader("📊 Live Payload Analytics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🧪 pH Level", f"{sensors.get('pH_level', 0.0):.2f}", sensors.get('pH_state', 'Unknown'), delta_color="off")
col2.metric("💧 Turbidity", f"{sensors.get('turbidity_percent', 0)}%")
col3.metric("🌡️ Air Temp", f"{sensors.get('temperature', 0.0)} °C")
col4.metric("🦇 Front Sonar", f"{sonar_dist} cm")

st.divider()

# ------------------------------------------
# ROW 2: PROPULSION & NAVIGATION
# ------------------------------------------
colA, colB = st.columns([1, 2])

# --- PROPULSION D-PAD & AUTO ---
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
    if st.button("🤖 INITIATE AUTO SWEEP (Serpentine)", use_container_width=True):
        send_command("AUTO")
    st.caption("Pressing any manual direction will instantly override the autopilot.")

# --- SATELLITE NAVIGATION MAP ---
with colB:
    st.subheader("🛰️ GPS Tracking")
    gps_data = fetch_data("gps")
    
    if gps_data and "lat" in gps_data and "lon" in gps_data:
        map_df = pd.DataFrame({'lat': [gps_data["lat"]], 'lon': [gps_data["lon"]]})
        st.map(map_df, zoom=18, use_container_width=True)
    else:
        st.info("📡 Awaiting Satellite Lock... (Ensure the NEO-6M antenna has a clear view of the sky)")
