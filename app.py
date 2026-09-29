import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Global Weather & Disaster Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1rem;
        color: #475569;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .landing-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Lunar Calculation Utility -----------------
def calculate_lunar_phase(date_obj):
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    if month < 3:
        year -= 1
        month += 12
    r = year % 100
    r = r / 19
    r = int(r)
    century_val = year // 100
    conway_val = (century_val - 15) * 11
    phase_val = (r * 11) - conway_val + month + day
    moon_age = (phase_val + 2) % 30
    
    if moon_age == 0 or moon_age == 29:
        return "New Moon (Amavasai)", "Max Spring Tide (High Flood Multiplier)"
    elif 1 <= moon_age <= 6:
        return "Waxing Crescent", "Moderate Gravitational Surge"
    elif moon_age == 7:
        return "First Quarter (Half Moon)", "Neap Tide (Minimal Sea Surge)"
    elif 8 <= moon_age <= 13:
        return "Waxing Gibbous", "Progressive Estuary Resistance"
    elif moon_age == 14 or moon_age == 15:
        return "Full Moon (Pournami)", "Max Spring Tide (Extreme Ocean Inundation)"
    elif 16 <= moon_age <= 21:
        return "Waning Gibbous", "High Gravitational Drag"
    elif moon_age == 22:
        return "Third Quarter (Half Moon)", "Neap Tide (Rapid River Discharge)"
    else:
        return "Waning Crescent", "Approaching Spring Alignment"

# ----------------- 4 Tabs Architecture -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Overview & Architecture",
    "🌐 Live Telemetry & 24h Rain Alert",
    "📜 2015–2026 Empirical Disaster DB",
    "🔮 Pattern-Driven Autonomous Forecaster"
])

# ================= TAB 1: LANDING INTERFACE =================
with tab1:
    st.markdown("""
    <div class="landing-card">
        <h2 style='color:#38bdf8; margin-top:0;'>Global Weather & Disaster Intelligence System</h2>
        <p style='font-size:1.05rem; line-height:1.6;'>
            An integrated meteorological and astrometric forecasting architecture designed for compound disaster risk analysis. 
            The system combines live atmospheric telemetry, 11-year empirical disaster records (2015–2026), 
            and lunar syzygy gravitation mechanics to predict inundation backwater barriers and industrial heat hazards.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <h4>🛰️ Layer 1: Atmospheric Telemetry</h4>
            <p>Real-time OpenWeatherMap REST API telemetry parsing temperature, humidity, wind velocity, and binary 24-hour PoP (Probability of Precipitation) rain advisories.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <h4>🌊 Layer 2: Lunar Syzygy Mechanics</h4>
            <p>Mathematical Conway lunar algorithm correlating Full Moon (Pournami) & New Moon (Amavasai) oceanic tidal surges with coastal drainage blockages.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card">
            <h4>🔥 Layer 3: Industrial Hazard Analytics</h4>
            <p>Historical correlation of summer heatwave vapor pressure spikes in chemical/manufacturing corridors with factory fires across Tamil Nadu.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📋 System Workflow & Verification")
    st.info("💡 **Navigation Guide:** Use the tabs above to test live weather data, inspect the 11-year auditable CSV database, or run autonomous future disaster risk simulations.")

# ================= TAB 2: LIVE WEATHER & RAIN ALERT =================
with tab2:
    st.subheader("Live Atmospheric Telemetry")
    city = st.text_input("Enter Target City / Region:", value="Chennai")
    
    if st.button("Fetch Live Weather Intelligence"):
        api_key = "bd5e378503939ddaee76f12ad7a97608" # Demo / standard key
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                current = data['list'][0]
                temp = current['main']['temp']
                humidity = current['main']['humidity']
                wind = current['wind']['speed']
                desc = current['weather'][0]['description'].capitalize()
                
                # Precipitation Probability Analysis
                pop_list = [item.get('pop', 0) for item in data['list'][:8]]
                max_pop = max(pop_list) if pop_list else 0
                rain_predicted = max_pop >= 0.20
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Temperature", f"{temp} °C")
                m2.metric("Humidity", f"{humidity} %")
                m3.metric("Wind Speed", f"{wind} m/s")
                m4.metric("Condition", desc)
                
                if rain_predicted:
                    st.error(f"🌧️ **Precipitation Advisory: RAIN PREDICTED (YES)** — Max 24h PoP Index: {int(max_pop * 100)}%")
                else:
                    st.success(f"☀️ **Precipitation Advisory: NO RAIN DETECTED** — Max 24h PoP Index: {int(max_pop * 100)}%")
            else:
                st.warning("City telemetry not found. Please verify spelling.")
        except Exception as e:
            st.error(f"Telemetry synchronization error: {e}")

# ================= TAB 3: EMPIRICAL DISASTER ARCHIVE =================
with tab3:
    st.subheader("11-Year Empirical Disaster Records (2015–2026)")
    disaster_records = [
        {"Year": 2015, "Location": "Chennai, Tamil Nadu", "Incident": "Chembarambakkam Urban Deluge", "Start": "2015-11-28", "End": "2015-12-05", "Days": 8, "Moon Phase": "Waning Gibbous (Syzygy)", "Impact": "Spring Tide Surge"},
        {"Year": 2016, "Location": "Chennai, Tamil Nadu", "Incident": "Severe Cyclone Vardah Landfall", "Start": "2016-12-12", "End": "2016-12-13", "Days": 2, "Moon Phase": "Full Moon (Pournami)", "Impact": "Peak Ocean Surge"},
        {"Year": 2018, "Location": "Kerala (All Basins)", "Incident": "Great Monsoonal Floods", "Start": "2018-08-08", "End": "2018-08-21", "Days": 14, "Moon Phase": "New Moon (Amavasai)", "Impact": "Max Astronomical Spring Tide"},
        {"Year": 2019, "Location": "Malappuram & Wayanad", "Incident": "Southwest Monsoon Landslide", "Start": "2019-08-08", "End": "2019-08-14", "Days": 7, "Moon Phase": "Waxing Crescent", "Impact": "Compound Runoff Obstruction"},
        {"Year": 2021, "Location": "Chennai, Tamil Nadu", "Incident": "Northeast Monsoon Urban Submersion", "Start": "2021-11-06", "End": "2021-11-12", "Days": 7, "Moon Phase": "Waxing Crescent", "Impact": "Tidal Ingress Retardation"},
        {"Year": 2022, "Location": "Silchar, Assam", "Incident": "Barak Valley Riverine Inundation", "Start": "2022-06-19", "End": "2022-06-26", "Days": 8, "Moon Phase": "Waning Gibbous", "Impact": "Estuary Drainage Gridlock"},
        {"Year": 2023, "Location": "Chennai, Tamil Nadu", "Incident": "Cyclone Michaung Inundation", "Start": "2023-12-03", "End": "2023-12-06", "Days": 4, "Moon Phase": "Waning Gibbous (Syzygy)", "Impact": "Spring Tide Runoff Reversal"},
        {"Year": 2024, "Location": "SIDCO Kakkalur, TN", "Incident": "Chemical Solvent Industrial Blaze", "Start": "2024-04-18", "End": "2024-04-19", "Days": 2, "Moon Phase": "First Quarter (Half Moon)", "Impact": "Summer Thermal Explosion"},
        {"Year": 2024, "Location": "Wayanad, Kerala", "Incident": "Chooralmala Mega Landslide", "Start": "2024-07-30", "End": "2024-08-03", "Days": 5, "Moon Phase": "Waning Crescent (Pre-New Moon)", "Impact": "Approaching Spring Alignment"},
        {"Year": 2026, "Location": "Red Hills, Tamil Nadu", "Incident": "Vadakarai Chemical Warehouse Blaze", "Start": "2026-03-02", "End": "2026-03-04", "Days": 3, "Moon Phase": "Full Moon (Pournami)", "Impact": "Industrial Thermal Spike"},
        {"Year": 2026, "Location": "Brahmaputra, Assam", "Incident": "Pre-Monsoon Basin Submersion", "Start": "2026-05-31", "End": "2026-06-07", "Days": 8, "Moon Phase": "Full Moon (Pournami)", "Impact": "Spring Tide Ingress Barrier"},
        {"Year": 2026, "Location": "Wayanad, Kerala", "Incident": "Southwest Monsoon Cloudburst", "Start": "2026-07-14", "End": "2026-07-19", "Days": 6, "Moon Phase": "New Moon (Amavasai)", "Impact": "Peak Syzygy Runoff Impedance"}
    ]
    df = pd.DataFrame(disaster_records)
    st.dataframe(df, use_container_width=True)
    
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Auditable Dataset (CSV)",
        data=csv_bytes,
        file_name="Global_Disaster_Database_2015_2026.csv",
        mime="text/csv"
    )

# ================= TAB 4: AUTONOMOUS FORECASTER =================
with tab4:
    st.subheader("Pattern-Driven Autonomous Risk Forecaster")
    target_loc = st.text_input("Enter Target Risk Region (e.g., Chennai, Kerala, Assam, Salem):", value="Chennai")
    
    if st.button("Generate Autonomous Hazard Projection"):
        now = datetime.now()
        found = False
        
        for d in range(1, 365):
            eval_date = now + timedelta(days=d)
            m = eval_date.month
            phase, tide = calculate_lunar_phase(eval_date)
            
            # Regional seasonal pattern matching
            is_monsoon = ("chennai" in target_loc.lower() and m in [10, 11, 12]) or \
                         ("kerala" in target_loc.lower() and m in [6, 7, 8]) or \
                         ("assam" in target_loc.lower() and m in [5, 6, 7])
            
            is_fire_season = m in [3, 4, 5, 6]
            
            if ("Amavasai" in phase or "Pournami" in phase) and (is_monsoon or is_fire_season):
                found = True
                end_date = eval_date + timedelta(days=5)
                st.markdown(f"### ⚠️ Projected Compound Hazard Window for **{target_loc}**")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Projected Start Date", eval_date.strftime("%Y-%m-%d"))
                c2.metric("Projected End Date", end_date.strftime("%Y-%m-%d"))
                c3.metric("Duration", "6 Days Window")
                
                st.warning(f"**Astrometric Trigger:** {phase} — {tide}")
                if is_monsoon:
                    st.info("🌧️ **Hydrological Threat:** Heavy rainfall synchronized with Syzygy ocean spring backwater will impede drainage canals.")
                else:
                    st.error("🔥 **Industrial Threat:** Peak heatwave evaporation and thermal conditions increase volatile chemical risks.")
                break
        
        if not found:
            st.success("No extreme compound astronomical risk windows detected for this query range.")
