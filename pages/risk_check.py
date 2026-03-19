import json, joblib
import numpy as np
import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download
import sys, os

# Ensure shared styles are accessible
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared_styles import (inject_styles, tokens, footer, page_header)

st.set_page_config(page_title="Risk Check", page_icon="🔮",
                   layout="wide", initial_sidebar_state="expanded")
inject_styles()
t = tokens()

# Force Streamlit widget labels to black for light theme visibility
st.markdown("""
    <style>
        label, label p, .st-emotion-cache-10trnc2 p, .st-emotion-cache-10trnc2 { 
            color: #000000 !important; 
        }
    </style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading prediction model…")
def load_model():
    # Note: Ensure these local paths exist or handle errors
    path    = hf_hub_download(repo_id="Prateek-1110/traffic_analyser",
                              filename="rf_model.pkl", repo_type="dataset")
    model   = joblib.load(path)
    encoder = joblib.load("models/label_encoder.pkl")
    with open("models/feature_meta.json") as f:
        meta = json.load(f)
    return model, encoder, meta

model, encoder, meta = load_model()

# ── Feature builder ───────────────────────────────────────────────────────────
def build_vector(lat, lon, hour, month, temp, humidity,
                 visibility, wind, precip, weather, junction, signal, crossing):
    def ssn(m):  return ("Winter" if m in [12,1,2] else "Spring" if m in [3,4,5]
                         else "Summer" if m in [6,7,8] else "Fall")
    def tod(h):  return ("Morning" if 5<=h<12 else "Afternoon" if 12<=h<17
                         else "Evening" if 17<=h<21 else "Night")
    
    sunrise = "Day" if 6 <= hour < 20 else "Night"
    row = {
        "Start_Lat": lat, "Start_Lng": lon,
        "Temperature(F)": temp, "Humidity(%)": humidity,
        "Visibility(mi)": visibility, "Wind_Speed(mph)": wind,
        "Precipitation(in)": precip,
        "Junction": int(junction), "Traffic_Signal": int(signal),
        "Crossing": int(crossing), "IsWeekend": 0,
        "Hour_sin":  np.sin(2*np.pi*hour/24),
        "Hour_cos":  np.cos(2*np.pi*hour/24),
        "Month_sin": np.sin(2*np.pi*month/12),
        "Month_cos": np.cos(2*np.pi*month/12),
    }
    for wg in meta["weather_groups"]:  row[f"WeatherGroup_{wg}"]   = int(weather==wg)
    for ss in meta["sunrise_sunset"]:  row[f"Sunrise_Sunset_{ss}"] = int(sunrise==ss)
    for s  in meta["seasons"]:         row[f"Season_{s}"]          = int(ssn(month)==s)
    for td in meta["time_of_day"]:     row[f"TimeOfDay_{td}"]      = int(tod(hour)==td)
    
    df_row = pd.DataFrame([row])
    for col in meta["features"]:
        if col not in df_row.columns: df_row[col] = 0
    return df_row[meta["features"]].fillna(0).astype(np.float32)

# ── Page header ───────────────────────────────────────────────────────────────
page_header("// 03 · risk predictor", "Risk Level Predictor",
            "Enter any location, time, and weather conditions → get predicted risk",
            t.get("accent3", "#6366f1"))

# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

# Helper for subheaders with improved light-theme contrast
def sub(label):
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                letter-spacing:.18em;color:#000000;opacity:0.7;
                text-transform:uppercase;margin:24px 0 8px;font-weight:600">
        {label}
    </div>
    """, unsafe_allow_html=True)

with left:
    sub("Location")
    lc1, lc2 = st.columns(2)
    lat = lc1.number_input("Latitude",  value=34.05,   step=0.0001, format="%.4f")
    lon = lc2.number_input("Longitude", value=-118.24, step=0.0001, format="%.4f")

    sub("Time")
    tc1, tc2 = st.columns(2)
    hour  = tc1.slider("Hour",  0, 23, 8,  format="%02d:00")
    month = tc2.slider("Month", 1, 12, 6)
    
    tod_s = ("Morning" if 5<=hour<12 else "Afternoon" if 12<=hour<17
             else "Evening" if 17<=hour<21 else "Night")
    ssn_s = ("Winter" if month in [12,1,2] else "Spring" if month in [3,4,5]
             else "Summer" if month in [6,7,8] else "Fall")
    
    # Improved visibility for the summary text
    st.markdown(f"""<div style="font-family:'JetBrains Mono',monospace;
        font-size:12px;color:#6366f1;margin-bottom:10px;font-weight:500">
        → {hour:02d}:00 &nbsp;·&nbsp; {tod_s} &nbsp;·&nbsp; {ssn_s}
    </div>""", unsafe_allow_html=True)

    sub("Weather")
    weather    = st.selectbox("Weather group", sorted(meta["weather_groups"]))
    wc1, wc2   = st.columns(2)
    temp       = wc1.number_input("Temperature (°F)", value=65.0)
    humidity   = wc2.number_input("Humidity (%)",     value=50.0)
    wc3, wc4   = st.columns(2)
    visibility = wc3.number_input("Visibility (mi)",    value=10.0, step=0.5)
    precip     = wc4.number_input("Precipitation (in)", value=0.0,  step=0.01)
    wind       = st.number_input("Wind speed (mph)", value=5.0)

    sub("Road features")
    rc1, rc2, rc3 = st.columns(3)
    junction = rc1.checkbox("Junction")
    signal   = rc2.checkbox("Traffic signal")
    crossing = rc3.checkbox("Crossing")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    run = st.button("→ Run prediction", type="primary", use_container_width=True)

# ── Result ────────────────────────────────────────────────────────────────────
with right:
    st.markdown(f"""<div style="font-family:'JetBrains Mono',monospace;font-size:11px;
        letter-spacing:.18em;color:#000000;opacity:0.7;
        text-transform:uppercase;margin-bottom:14px;font-weight:600">Result</div>""",
        unsafe_allow_html=True)

    if not run:
        # Fixed "awaiting input" card for light theme visibility
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.03);border:1px dashed rgba(0,0,0,0.1);
                    border-radius:14px;padding:48px 24px;text-align:center">
            <div style="font-size:40px;margin-bottom:12px;opacity:.2;color:#000000">◈</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:12px;
                        letter-spacing:.08em;color:#000000;opacity:0.6">
                AWAITING INPUT
            </div>
            <div style="font-size:13px;margin-top:24px;
                        color:#000000;opacity:0.8;line-height:1.9;text-align:left;
                        border-top:1px solid rgba(0,0,0,0.05);padding-top:16px">
                <b>Examples:</b><br>
                ❄️ Snow/Ice · 23:00 · junction → High risk<br>
                ☀️ Clear · 14:00 · visibility 10mi → Low risk<br>
                🌧️ Rain · 08:00 · low visibility → High risk
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        with st.spinner("Running model…"):
            vec      = build_vector(lat, lon, hour, month, temp, humidity,
                                    visibility, wind, precip, weather,
                                    junction, signal, crossing)
            pred_enc = model.predict(vec)[0]
            proba    = model.predict_proba(vec)[0]
            risk     = encoder.inverse_transform([pred_enc])[0]
            conf     = float(proba.max()) * 100
            probs    = {cls: round(float(p)*100, 1)
                        for cls, p in zip(encoder.classes_, proba)}

        # Color mapping optimized for both light and dark
        # Using RGBA for card backgrounds ensures readability regardless of theme
        EMOJI = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        COLOR = {"High": "#d00000", "Medium": "#e85d04", "Low": "#2b9348"}
        BG_COLOR = {"High": "#ffccd5", "Medium": "#fee44022", "Low": "#d8f3dc"}

        st.markdown(f"""
        <div style="background:{BG_COLOR[risk]};border:1px solid {COLOR[risk]}44;
                    border-left:5px solid {COLOR[risk]};border-radius:14px;
                    padding:32px 28px;text-align:center;margin-bottom:24px">
            <div style="font-size:52px;margin-bottom:10px;line-height:1">
                {EMOJI[risk]}
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:2.2rem;
                        font-weight:800;color:{COLOR[risk]};
                        letter-spacing:-.01em;margin-bottom:6px;line-height:1">
                {risk} Risk
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:12px;
                        color:{COLOR[risk]};letter-spacing:.12em;
                        text-transform:uppercase;font-weight:600">
                confidence · {conf:.1f}%
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div style="font-family:'JetBrains Mono',monospace;
            font-size:11px;letter-spacing:0.1em;color:#000000;
            text-transform:uppercase;margin-bottom:16px;font-weight:600">
            Probability breakdown</div>""", unsafe_allow_html=True)

        for cls, clr in [("High","#d00000"), ("Medium","#e85d04"), ("Low", "#2b9348")]:
            p = probs.get(cls, 0)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
                <div style="width:65px;font-family:'JetBrains Mono',monospace;
                            font-size:11px;color:{clr};font-weight:bold">{cls}</div>
                <div style="flex:1;background:rgba(0,0,0,0.05);border-radius:99px;
                            height:8px;overflow:hidden;border:1px solid rgba(0,0,0,0.05)">
                    <div style="width:{p}%;background:{clr};
                                height:100%;border-radius:99px"></div>
                </div>
                <div style="width:45px;font-family:'JetBrains Mono',monospace;
                            font-size:11px;color:#000000;text-align:right;font-weight:600">{p}%</div>
            </div>""", unsafe_allow_html=True)

        with st.expander("View Input Summary"):
            feats = [f for f, v in [("Junction", junction),
                                     ("Traffic signal", signal),
                                     ("Crossing", crossing)] if v]
            st.table(pd.DataFrame({
                "Field": ["Location", "Time", "Weather", "Temp/Hum", "Visibility", "Wind", "Road"],
                "Value": [
                    f"{lat:.4f}, {lon:.4f}",
                    f"{hour:02d}:00 ({tod_s})",
                    weather,
                    f"{temp}°F / {humidity}%",
                    f"{visibility} mi (Precip: {precip}in)",
                    f"{wind} mph",
                    ', '.join(feats) or "Standard Road"
                ]
            }))

footer()