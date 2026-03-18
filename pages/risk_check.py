import json, joblib
import numpy as np
import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared_styles import (init_theme, inject_styles, tokens, footer,
                           theme_toggle, page_header,get_theme)

st.set_page_config(page_title="Risk Check", page_icon="🔮",
                   layout="wide", initial_sidebar_state="expanded")
init_theme()
inject_styles()
t = tokens()

# theme_toggle()

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading prediction model…")
def load_model():
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
            t["accent3"])

# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

def sub(label):
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                letter-spacing:.18em;color:{t['accent3']};
                text-transform:uppercase;margin:14px 0 8px">{label}</div>
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
    st.markdown(f"""<div style="font-family:'JetBrains Mono',monospace;
        font-size:11px;color:{t['accent']};margin-bottom:4px">
        → {hour:02d}:00 &nbsp;·&nbsp; {tod_s} &nbsp;·&nbsp; {ssn_s}
    </div>""", unsafe_allow_html=True)

    sub("Weather")
    weather    = st.selectbox("Weather group", sorted(meta["weather_groups"]),
                              label_visibility="collapsed")
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

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    run = st.button("→ Run prediction", type="primary", use_container_width=True)

# ── Result ────────────────────────────────────────────────────────────────────
with right:
    st.markdown(f"""<div style="font-family:'JetBrains Mono',monospace;font-size:10px;
        letter-spacing:.18em;color:{t['accent3']};
        text-transform:uppercase;margin-bottom:14px">Result</div>""",
        unsafe_allow_html=True)

    if not run:
        st.markdown(f"""
        <div style="background:{t['bg2']};border:1px solid {t['border']};
                    border-radius:14px;padding:36px 24px;text-align:center">
            <div style="font-size:40px;margin-bottom:12px;
                        opacity:.3;color:{t['text_m']}">◈</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:12px;
                        letter-spacing:.08em;color:{t['text_m']}">awaiting input</div>
            <div style="font-size:12px;margin-top:24px;
                        color:{t['text_dim']};line-height:1.9;text-align:left;
                        border-top:1px solid {t['border']};padding-top:16px">
                Snow/Ice · 23:00 · junction → High risk<br>
                Clear · 14:00 · visibility 10mi → Low risk<br>
                Rain · 08:00 · low visibility → High risk
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

        is_dark = st.session_state.get("theme", "dark") == "dark"
        EMOJI = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        COLOR = {"High": "#e63946", "Medium": "#f4a261", "Low": t["accent"]}
        card_bg = t[f"card_{'high' if risk=='High' else 'med' if risk=='Medium' else 'low'}"]

        st.markdown(f"""
        <div style="background:{card_bg};border:1px solid {COLOR[risk]}33;
                    border-left:3px solid {COLOR[risk]};border-radius:14px;
                    padding:32px 28px;text-align:center;margin-bottom:20px">
            <div style="font-size:52px;margin-bottom:10px;line-height:1">
                {EMOJI[risk]}
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:2.2rem;
                        font-weight:800;color:{COLOR[risk]};
                        letter-spacing:-.01em;margin-bottom:6px;line-height:1">
                {risk} Risk
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                        color:{COLOR[risk]}88;letter-spacing:.12em;
                        text-transform:uppercase">
                confidence · {conf:.1f}%
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div style="font-family:'JetBrains Mono',monospace;
            font-size:10px;letter-spacing:.18em;color:{t['text_m']};
            text-transform:uppercase;margin-bottom:12px">
            Probability breakdown</div>""", unsafe_allow_html=True)

        for cls, clr in [("High","#e63946"), ("Medium","#f4a261"), ("Low", t["accent"])]:
            p = probs.get(cls, 0)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">
                <div style="width:56px;font-family:'JetBrains Mono',monospace;
                            font-size:11px;color:{clr}">{cls}</div>
                <div style="flex:1;background:{t['bg3']};border-radius:99px;
                            height:6px;overflow:hidden;border:1px solid {t['border']}">
                    <div style="width:{p}%;background:{clr};
                                height:100%;border-radius:99px"></div>
                </div>
                <div style="width:40px;font-family:'JetBrains Mono',monospace;
                            font-size:11px;color:{clr};text-align:right">{p}%</div>
            </div>""", unsafe_allow_html=True)

        with st.expander("Input summary"):
            feats = [f for f, v in [("Junction", junction),
                                     ("Traffic signal", signal),
                                     ("Crossing", crossing)] if v]
            st.markdown(f"""
| Field | Value |
|---|---|
| Location | `{lat:.4f}, {lon:.4f}` |
| Time | `{hour:02d}:00` · {tod_s} · {ssn_s} |
| Weather | {weather} |
| Temp / Humidity | {temp}°F / {humidity}% |
| Visibility | {visibility} mi · Precip {precip} in |
| Wind | {wind} mph |
| Road features | {', '.join(feats) or 'None'} |
            """)

footer()