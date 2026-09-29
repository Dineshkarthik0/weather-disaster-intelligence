import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="Global Disaster Intelligence & Lunar System", page_icon="🌐", layout="wide")

st.markdown("""
<style>
.info-card {
    background-color: #1e293b;
    border-radius: 8px;
    padding: 12px;
    color: #f8fafc;
    margin-bottom: 8px;
}
.info-title {
    font-size: 11px;
    color: #94a3b8;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.info-val {
    font-size: 18px;
    font-weight: 700;
    color: #38bdf8;
}
.disaster-box {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    color: #f8fafc;
}
</style>
""", unsafe_allow_html=True)

# Lunar Phase Engine (Conway's Method)
def get_lunar_phase(date_val):
    year = date_val.year
    month = date_val.month
    day = date_val.day
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
        return "New Moon (Amavasai)", "Max Spring Tide (High Tidal Backwater Surge)"
    elif 1 <= moon_age <= 6:
        return "Waxing Crescent", "Moderate Gravitational Surge"
    elif moon_age == 7:
        return "First Quarter (Half Moon)", "Neap Tide (Minimal Sea Surge)"
    elif 8 <= moon_age <= 13:
        return "Waxing Gibbous", "Progressive Estuary Resistance"
    elif moon_age == 14 or moon_age == 15:
        return "Full Moon (Pournami)", "Max Spring Tide (High Astronomical Inundation)"
    elif 16 <= moon_age <= 21:
        return "Waning Gibbous", "High Gravitational Backwater Resistance"
    elif moon_age == 22:
        return "Third Quarter (Half Moon)", "Neap Tide (Fast Runoff Discharge)"
    else:
        return "Waning Crescent", "Approaching Spring Alignment"

tab1, tab2, tab3 = st.tabs([
    "🌐 Live Weather & Rain Alert",
    "📜 2015–2026 Empirical Disaster DB",
    "🔮 Pattern-Driven Autonomous Forecaster"
])

# ----------------- TAB 1: LIVE WEATHER -----------------
with tab1:
    st.subheader("Global Live Meteorological Telemetry")
    col_input, _ = st.columns([2, 1])
    with col_input:
        target_city = st.text_input("Enter City / Region:", value="Chennai")
        check_weather = st.button("Query Real-Time Telemetry")

    if check_weather:
        api_key = "bd5e378503939ddaee76f12ad7a97608"
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={target_city}&appid={api_key}&units=metric"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                cur = data["list"][0]
                temp = cur["main"]["temp"]
                hum = cur["main"]["humidity"]
                wind = cur["wind"]["speed"]
                desc = cur["weather"][0]["description"].title()
                
                # Check 24-hr PoP (8 slots of 3 hours)
                slots = data["list"][:8]
                pop_list = [s.get("pop", 0.0) for s in slots]
                max_pop = max(pop_list) if pop_list else 0.0
                rain_predicted = max_pop >= 0.20
                
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f'<div class="info-card"><div class="info-title">Temperature</div><div class="info-val">{temp} °C</div></div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="info-card"><div class="info-title">Humidity</div><div class="info-val">{hum} %</div></div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="info-card"><div class="info-title">Wind Speed</div><div class="info-val">{wind} m/s</div></div>', unsafe_allow_html=True)
                c4.markdown(f'<div class="info-card"><div class="info-title">Condition</div><div class="info-val">{desc}</div></div>', unsafe_allow_html=True)
                
                st.markdown("---")
                if rain_predicted:
                    st.error(f"🌧️ **Precipitation Advisory: RAIN PREDICTED (YES)** — 24-Hour Max PoP: {int(max_pop * 100)}%")
                else:
                    st.success(f"☀️ **Precipitation Advisory: NO RAIN DETECTED** — 24-Hour Max PoP: {int(max_pop * 100)}%")
            else:
                st.warning("City telemetry not found. Please check spelling.")
        except Exception as e:
            st.error(f"API connection error: {e}")

# ----------------- TAB 2: EMPIRICAL DB (2015-2026) -----------------
with tab2:
    st.subheader("11-Year Empirical Disaster Intelligence (2015–2026)")
    disaster_dataset = [
        {"Year": 2015, "Location": "Chennai, Tamil Nadu", "Incident": "Chembarambakkam Reservoir Urban Deluge", "Start": "2015-11-28", "End": "2015-12-05", "Duration": "8 Days", "Moon Phase": "Waning Gibbous (Syzygy)", "Impact": "Spring Tide Surge"},
        {"Year": 2016, "Location": "Chennai, Tamil Nadu", "Incident": "Cyclone Vardah Landfall", "Start": "2016-12-12", "End": "2016-12-13", "Duration": "2 Days", "Moon Phase": "Full Moon (Pournami)", "Impact": "High Tidal Surge"},
        {"Year": 2017, "Location": "Ockhi Corridor, TN & KL", "Incident": "Very Severe Cyclonic Storm Ockhi", "Start": "2017-11-29", "End": "2017-12-04", "Duration": "6 Days", "Moon Phase": "Waxing Gibbous", "Impact": "Extreme Sea Roughness"},
        {"Year": 2018, "Location": "Kerala (All Basins)", "Incident": "Great Monsoonal Floods", "Start": "2018-08-08", "End": "2018-08-21", "Duration": "14 Days", "Moon Phase": "New Moon (Amavasai)", "Impact": "Max Astronomical Spring Tide"},
        {"Year": 2019, "Location": "Malappuram & Wayanad, KL", "Incident": "Southwest Monsoon Landslide & Flood", "Start": "2019-08-08", "End": "2019-08-14", "Duration": "7 Days", "Moon Phase": "Waxing Crescent", "Impact": "Drainage Obstruction"},
        {"Year": 2020, "Location": "Tamil Nadu Coastal Belt", "Incident": "Very Severe Cyclonic Storm Nivar", "Start": "2020-11-24", "End": "2020-11-27", "Duration": "4 Days", "Moon Phase": "Waxing Gibbous", "Impact": "Tidal Ingress"},
        {"Year": 2021, "Location": "Chennai, Tamil Nadu", "Incident": "Northeast Monsoon Urban Submersion", "Start": "2021-11-06", "End": "2021-11-12", "Duration": "7 Days", "Moon Phase": "Waxing Crescent", "Impact": "Drainage Gridlock"},
        {"Year": 2022, "Location": "Silchar, Assam", "Incident": "Barak Valley Riverine Inundation", "Start": "2022-06-19", "End": "2022-06-26", "Duration": "8 Days", "Moon Phase": "Waning Gibbous", "Impact": "River Ingress Barrier"},
        {"Year": 2023, "Location": "Chennai, Tamil Nadu", "Incident": "Cyclone Michaung Catastrophic Flooding", "Start": "2023-12-03", "End": "2023-12-06", "Duration": "4 Days", "Moon Phase": "Waning Gibbous (Syzygy)", "Impact": "Spring Tide Barrier"},
        {"Year": 2023, "Location": "Kahramanmaras, Turkey", "Incident": "Anatolian Continental Earthquake", "Start": "2023-02-06", "End": "2023-02-06", "Duration": "1 Day", "Moon Phase": "Full Moon (Pournami)", "Impact": "Compound Astrometric Stress"},
        {"Year": 2024, "Location": "Noto Peninsula, Japan", "Incident": "Offshore Subduction Earthquake & Tsunami", "Start": "2024-01-01", "End": "2024-01-02", "Duration": "2 Days", "Moon Phase": "Waning Gibbous", "Impact": "Tidal Wave Amplification"},
        {"Year": 2024, "Location": "SIDCO Kakkalur, TN", "Incident": "Chemical Solvent Industrial Blaze", "Start": "2024-04-18", "End": "2024-04-19", "Duration": "2 Days", "Moon Phase": "First Quarter (Half Moon)", "Impact": "Summer Thermal Explosion"},
        {"Year": 2024, "Location": "Dubai, UAE", "Incident": "Cloudburst Flash Flooding Inundation", "Start": "2024-04-16", "End": "2024-04-17", "Duration": "2 Days", "Moon Phase": "First Quarter (Half Moon)", "Impact": "Urban Drainage Saturation"},
        {"Year": 2024, "Location": "Gummidipoondi, TN", "Incident": "Chemical Synthetic Resin Industrial Fire", "Start": "2024-05-22", "End": "2024-05-23", "Duration": "2 Days", "Moon Phase": "Full Moon (Pournami)", "Impact": "Peak Atmospheric Heat Expansion"},
        {"Year": 2024, "Location": "Wayanad, Kerala", "Incident": "Chooralmala Mega Landslide", "Start": "2024-07-30", "End": "2024-08-03", "Duration": "5 Days", "Moon Phase": "Waning Crescent (Pre-New Moon)", "Impact": "Approaching Spring Alignment"},
        {"Year": 2025, "Location": "California, USA", "Incident": "Diablo Wind Urban Firestorms", "Start": "2025-01-07", "End": "2025-01-14", "Duration": "8 Days", "Moon Phase": "Waxing Gibbous", "Impact": "Dry Gale Thermal Front"},
        {"Year": 2026, "Location": "Red Hills, Tamil Nadu", "Incident": "Vadakarai Chemical Warehouse Blaze", "Start": "2026-03-02", "End": "2026-03-04", "Duration": "3 Days", "Moon Phase": "Full Moon (Pournami)", "Impact": "Industrial Thermal Spike"},
        {"Year": 2026, "Location": "Manali Corridor, TN", "Incident": "Petrochemical Pipeline Thermal Detonation", "Start": "2026-04-11", "End": "2026-04-13", "Duration": "3 Days", "Moon Phase": "Third Quarter (Half Moon)", "Impact": "Vapor Pressure Buildup"},
        {"Year": 2026, "Location": "Brahmaputra Basin, Assam", "Incident": "Pre-Monsoon Basin Submersion", "Start": "2026-05-31", "End": "2026-06-07", "Duration": "8 Days", "Moon Phase": "Full Moon (Pournami)", "Impact": "Spring Tide Ingress Barrier"},
        {"Year": 2026, "Location": "Wayanad, Kerala", "Incident": "Southwest Monsoon Cloudburst Deluge", "Start": "2026-07-14", "End": "2026-07-19", "Duration": "6 Days", "Moon Phase": "New Moon (Amavasai)", "Impact": "Peak Syzygy Drainage Impedance"}
    ]
    df_db = pd.DataFrame(disaster_dataset)
    st.dataframe(df_db, use_container_width=True)
    
    csv_bytes = df_db.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Full Dataset (CSV)",
        data=csv_bytes,
        file_name="Global_Disaster_Database_2015_2026.csv",
        mime="text/csv"
    )

# ----------------- TAB 3: AUTONOMOUS FORECASTER -----------------
with tab3:
    st.subheader("Autonomous Astronomical & Regional Hazard Forecaster")
    target_area = st.text_input("Enter Target Risk Region (e.g., Chennai, Kerala, Salem, Assam):", value="Chennai")
    
    if st.button("Compute Autonomous Horizon"):
        now_date = datetime.now()
        detected = False
        
        for offset in range(1, 365):
            eval_date = now_date + timedelta(days=offset)
            m = eval_date.month
            phase_name, tide_impact = get_lunar_phase(eval_date)
            
            is_monsoon = ("chennai" in target_area.lower() and m in [10, 11, 12]) or \
                         ("kerala" in target_area.lower() and m in [6, 7, 8]) or \
                         ("assam" in target_area.lower() and m in [5, 6, 7])
            
            is_fire_season = m in [3, 4, 5, 6]
            
            if ("Amavasai" in phase_name or "Pournami" in phase_name) and (is_monsoon or is_fire_season):
                detected = True
                end_eval_date = eval_date + timedelta(days=5)
                
                st.markdown(f"""
                <div class="disaster-box">
                    <h3 style="color: #38bdf8; margin-top:0;">Projected Risk Span for {target_area}</h3>
                    <p><b>Timeline:</b> {eval_date.strftime('%Y-%m-%d')} to {end_eval_date.strftime('%Y-%m-%d')} (6 Days Window)</p>
                    <p><b>Astrometric Phase:</b> {phase_name}</p>
                    <p><b>Tidal Force Influence:</b> {tide_impact}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if is_monsoon:
                    st.info("🌧️ **Hydrological Threat:** High rainfall synchronized with Syzygy ocean high-tide will trap inland river runoff.")
                else:
                    st.error("🔥 **Industrial Threat:** Summer peak vapor pressure increases factory boiler/chemical hazard probability.")
                break
        
        if not detected:
            st.success("No critical compound astronomical window detected within the scan range.")
