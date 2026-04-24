import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="S.A.G.A.R. HUD", layout="wide", page_icon="🛥️")
FIREBASE_BASE = "https://sagar-cloud-default-rtdb.firebaseio.com"

# --- CUSTOM THEME STYLING ---
st.markdown("""
    <style>
    /* Ocean/Naval Theme Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a1e3e 0%, #1a3a52 50%, #0d2636 100%);
        color: #e0e8f0;
    }
    
    /* Main content area */
    [data-testid="stMainBlockContainer"] {
        background: rgba(10, 30, 62, 0.85);
    }
    
    /* Headers and text */
    h1, h2, h3 {
        color: #00d4ff !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        font-weight: 700;
    }
    
    p, span, label {
        color: #b0c4de !important;
    }
    
    /* Dividers */
    hr {
        border-color: #00d4ff !important;
        opacity: 0.5;
    }
    
    /* Buttons */
    button[kind="primary"], button[kind="secondary"] {
        background: linear-gradient(135deg, #0088cc, #00bfff) !important;
        color: white !important;
        border: 1px solid #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.3) !important;
    }
    
    button[kind="primary"]:hover, button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #005a8d, #0099cc) !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.6) !important;
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(0, 136, 204, 0.15), rgba(0, 191, 255, 0.1)) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px;
        padding: 15px;
        box-shadow: inset 0 0 10px rgba(0, 212, 255, 0.1);
    }
    
    /* Info/Success/Error boxes */
    .stAlert {
        background: linear-gradient(135deg, rgba(0, 136, 204, 0.2), rgba(0, 191, 255, 0.15)) !important;
        border: 1px solid #00d4ff !important;
        color: #b0c4de !important;
    }
    
    .stAlert > div:first-child {
        color: #00d4ff !important;
    }
    
    /* Columns and containers */
    [data-testid="column"] {
        background: rgba(26, 58, 82, 0.4);
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Input fields */
    input, textarea, select {
        background: rgba(10, 30, 62, 0.6) !important;
        color: #b0c4de !important;
        border: 1px solid #00d4ff !important;
        border-radius: 5px;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(10, 30, 62, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00d4ff;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00a8cc;
    }
    </style>
""", unsafe_allow_html=True)

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

# --- SATELLITE NAVIGATION MAP (DEMO MODE) ---
with colB:
    st.subheader("🛰️ Navigation & GPS Tracking")
    
    # 🧭 COMPASS DISPLAY
    heading = sensors.get('compass_heading', 0)
    cardinal = get_cardinal_direction(heading)
    st.info(f"**🧭 Current Magnetic Heading:** {heading}° ({cardinal})")
    
    # 📍 EXAM DEMO MODE MAP
    # Ensure these are pure numbers with NO quotes and NO commas at the end
    COLLEGE_LAT = 19.0430  
    COLLEGE_LON = 73.0230  
    
    # Force the values to be floats to prevent Streamlit rendering errors
    map_df = pd.DataFrame({
        'lat': [float(COLLEGE_LAT)], 
        'lon': [float(COLLEGE_LON)]
    })
    
    # Render map without the zoom parameter to force auto-centering
    st.map(map_df, use_container_width=True)
    st.success("🛰️ GPS Lock Secured: Coordinates Locked to Campus (Simulation)")
