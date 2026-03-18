import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download

st.set_page_config(page_title="Risk Check", page_icon="🔮", layout="wide")

st.title("🔮 Risk Level Predictor")
st.caption("Enter any location, time, and weather → get predicted accident risk")

# ── Download model from Hugging Face (cached after first load) ────────────────
@st.cache_resource(show_spinner="Loading prediction model from Hugging Face...")
def load_model():
    model_path = hf_hub_download(
        repo_id="Prateek-1110/traffic_analyser",
        filename="rf_model.pkl",
        repo_type="dataset",
    )
    model = joblib.load(model_path)

    # label_encoder and feature_meta live in repo (small files)
    encoder = joblib.load("models/label_encoder.pkl")
    with open("models/feature_meta.json") as f:
        meta = json.load(f)

    return model, encoder, meta

model, encoder, meta = load_model()

# ── Feature builder (mirrors notebook 03) ────────────────────────────────────
def build_vector(lat, lon, hour, month, temp, humidity,
                 visibility, wind, precip, weather,
                 junction, signal, crossing):

    def get_season(m):
        if m in [12,1,2]: return "Winter"
        if m in [3,4,5]:  return "Spring"
        if m in [6,7,8]:  return "Summer"
        return "Fall"

    def get_tod(h):
        if 5  <= h < 12: return "Morning"
        if 12 <= h < 17: return "Afternoon"
        if 17 <= h < 21: return "Evening"
        return "Night"

    sunrise = "Day" if 6 <= hour < 20 else "Night"

    row = {
        "Start_Lat": lat, "Start_Lng": lon,
        "Temperature(F)": temp, "Humidity(%)": humidity,
        "Visibility(mi)": visibility, "Wind_Speed(mph)": wind,
        "Precipitation(in)": precip,
        "Junction": int(junction), "Traffic_Signal": int(signal),
        "Crossing": int(crossing), "IsWeekend": 0,
        "Hour_sin":  np.sin(2 * np.pi * hour  / 24),
        "Hour_cos":  np.cos(2 * np.pi * hour  / 24),
        "Month_sin": np.sin(2 * np.pi * month / 12),
        "Month_cos": np.cos(2 * np.pi * month / 12),
    }
    for wg in meta["weather_groups"]:
        row[f"WeatherGroup_{wg}"] = int(weather == wg)
    for ss in meta["sunrise_sunset"]:
        row[f"Sunrise_Sunset_{ss}"] = int(sunrise == ss)
    for s in meta["seasons"]:
        row[f"Season_{s}"] = int(get_season(month) == s)
    for t in meta["time_of_day"]:
        row[f"TimeOfDay_{t}"] = int(get_tod(hour) == t)

    df = pd.DataFrame([row])
    for col in meta["features"]:
        if col not in df.columns:
            df[col] = 0
    return df[meta["features"]].fillna(0).astype(np.float32)


# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("#### Location")
    lc1, lc2 = st.columns(2)
    lat = lc1.number_input("Latitude",  value=34.05,   step=0.0001, format="%.4f")
    lon = lc2.number_input("Longitude", value=-118.24, step=0.0001, format="%.4f")

    st.markdown("#### Time")
    tc1, tc2 = st.columns(2)
    hour  = tc1.slider("Hour (0–23)",  0, 23, 8)
    month = tc2.slider("Month (1–12)", 1, 12, 6)

    tod = ("Morning" if 5<=hour<12
           else "Afternoon" if 12<=hour<17
           else "Evening" if 17<=hour<21
           else "Night")
    season = ("Winter" if month in [12,1,2]
              else "Spring" if month in [3,4,5]
              else "Summer" if month in [6,7,8]
              else "Fall")
    st.caption(f"→ {tod}, {season}")

    st.markdown("#### Weather")
    weather    = st.selectbox("Weather group", sorted(meta["weather_groups"]))
    wc1, wc2   = st.columns(2)
    temp       = wc1.number_input("Temperature (°F)", value=65.0)
    humidity   = wc2.number_input("Humidity (%)",     value=50.0)
    wc3, wc4   = st.columns(2)
    visibility = wc3.number_input("Visibility (mi)",    value=10.0, step=0.5)
    precip     = wc4.number_input("Precipitation (in)", value=0.0,  step=0.01)
    wind       = st.number_input("Wind speed (mph)", value=5.0)

    st.markdown("#### Road features")
    rc1, rc2, rc3 = st.columns(3)
    junction = rc1.checkbox("Junction")
    signal   = rc2.checkbox("Traffic signal")
    crossing = rc3.checkbox("Crossing")

    st.markdown("")
    predict_btn = st.button("Predict risk level", type="primary", use_container_width=True)

# ── Result ────────────────────────────────────────────────────────────────────
with right:
    st.markdown("#### Result")

    if not predict_btn:
        st.info("Fill in the form and click **Predict risk level**")
        st.markdown("""
**Try these scenarios to test the model:**

| Scenario | Expected |
|---|---|
| Rain + hour 8 + visibility 2mi | High |
| Clear + hour 14 + visibility 10mi | Low |
| Snow/Ice + hour 23 + junction | High |
| Fog + hour 5 + crossing | Medium–High |
        """)
    else:
        with st.spinner("Running model..."):
            vec      = build_vector(lat, lon, hour, month, temp, humidity,
                                    visibility, wind, precip, weather,
                                    junction, signal, crossing)
            pred_enc = model.predict(vec)[0]
            proba    = model.predict_proba(vec)[0]
            risk     = encoder.inverse_transform([pred_enc])[0]
            conf     = float(proba.max()) * 100
            probs    = {cls: round(float(p)*100, 1)
                        for cls, p in zip(encoder.classes_, proba)}

        EMOJI = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        COLOR = {"High": "#e63946", "Medium": "#f4a261", "Low": "#2a9d8f"}

        st.markdown(f"""
<div style="
    background:#1a1d27;
    border:1px solid #2e3248;
    border-left:4px solid {COLOR[risk]};
    border-radius:12px;
    padding:28px 24px;
    text-align:center;
    margin-bottom:16px;
">
    <div style="font-size:48px;margin-bottom:8px">{EMOJI[risk]}</div>
    <div style="font-size:28px;font-weight:800;color:{COLOR[risk]};margin-bottom:4px">
        {risk} Risk
    </div>
    <div style="color:#7b82a8;font-size:13px">
        Model confidence: {conf:.1f}%
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("**Probability breakdown**")
        for cls, clr in [("High","#e63946"),("Medium","#f4a261"),("Low","#2a9d8f")]:
            p = probs.get(cls, 0)
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
    <div style="width:60px;font-size:12px;color:#7b82a8">{cls}</div>
    <div style="flex:1;background:#22263a;border-radius:99px;height:8px;overflow:hidden">
        <div style="width:{p}%;background:{clr};height:100%;border-radius:99px"></div>
    </div>
    <div style="width:44px;font-size:12px;text-align:right">{p}%</div>
</div>
""", unsafe_allow_html=True)

        with st.expander("Input summary"):
            features_used = [
                f for f, v in [
                    ("Junction", junction),
                    ("Traffic signal", signal),
                    ("Crossing", crossing)
                ] if v
            ]
            st.markdown(f"""
| Field | Value |
|---|---|
| Location | {lat:.4f}, {lon:.4f} |
| Time | {hour:02d}:00 ({tod}), {season} |
| Weather | {weather} |
| Temperature | {temp}°F |
| Visibility | {visibility} mi |
| Precipitation | {precip} in |
| Wind | {wind} mph |
| Road features | {', '.join(features_used) or 'None'} |
            """)