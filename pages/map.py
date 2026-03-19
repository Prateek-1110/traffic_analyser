import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared_styles import inject_styles, tokens, footer, page_header, section_label

st.set_page_config(page_title="Hotspot Map", page_icon="🗺",
                   layout="wide", initial_sidebar_state="expanded")
inject_styles()
t = tokens()

@st.cache_data
def load_hotspots():
    return pd.read_csv("data/hotspot_summary.csv")

df = load_hotspots()
cities   = ["All"] + sorted(df["City"].unique().tolist())
city_sel = st.sidebar.selectbox("Filter by city", cities)
risk_sel = st.sidebar.multiselect(
    "Risk level", ["High", "Medium", "Low"],
    default=["High", "Medium", "Low"]
)

# ── Filter ────────────────────────────────────────────────────────────────────
filtered = df.copy()
if city_sel != "All":
    filtered = filtered[filtered["City"] == city_sel]
filtered = filtered[filtered["Risk"].isin(risk_sel)]

# ── Header ────────────────────────────────────────────────────────────────────
page_header("// 01 · hotspot map", "Accident Hotspot Map",
            "DBSCAN clusters across top US cities · click any circle for details",
            t["accent"])

# ── Stats ─────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total hotspots",  len(filtered))
c2.metric("🔴 High",   int((filtered["Risk"] == "High").sum()))
c3.metric("🟡 Medium", int((filtered["Risk"] == "Medium").sum()))
c4.metric("🟢 Low",    int((filtered["Risk"] == "Low").sum()))
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Map ───────────────────────────────────────────────────────────────────────
RISK_COLORS = {"High": "#e63946", "Medium": "#f4a261", "Low": "#2a9d8f"}
tile = "CartoDB dark_matter"

clat = filtered["Lat"].mean() if len(filtered) else 37.8
clng = filtered["Lng"].mean() if len(filtered) else -96.0

m = folium.Map(location=[clat, clng],
               zoom_start=5 if city_sel == "All" else 11,
               tiles=tile)

if len(filtered) > 0:
    HeatMap(filtered[["Lat", "Lng", "Count"]].values.tolist(),
            min_opacity=0.25, radius=20, blur=14,
            gradient={0.2: "#1a2a4a", 0.5: "#f4a261", 1.0: "#e63946"}).add_to(m)

for _, row in filtered.iterrows():
    if pd.isna(row["Lat"]) or pd.isna(row["Lng"]): continue
    color  = RISK_COLORS.get(row["Risk"], "#888")
    radius = 8 + min(row["Count"] / 30, 28)
    popup_html = f"""
    <div style='font-size:13px;min-width:200px;padding:4px'>
        <div style='font-weight:700;color:{color};margin-bottom:8px'>
            {row['Risk']} Risk Hotspot
        </div>
        <table style='width:100%;border-collapse:collapse;font-size:12px'>
            <tr><td style='color:#888;padding:3px 0'>City</td>
                <td>{row['City']}</td></tr>
            <tr><td style='color:#888;padding:3px 0'>Accidents</td>
                <td>{int(row['Count']):,}</td></tr>
            <tr><td style='color:#888;padding:3px 0'>Mean severity</td>
                <td>{row['Mean_Severity']}</td></tr>
            <tr><td style='color:#888;padding:3px 0'>Peak hour</td>
                <td>{str(int(row['Peak_Hour'])).zfill(2)}:00</td></tr>
            <tr><td style='color:#888;padding:3px 0'>Weather</td>
                <td>{row['Weather']}</td></tr>
        </table>
    </div>"""
    folium.CircleMarker(
        location=[row["Lat"], row["Lng"]],
        radius=radius, color=color, fill=True,
        fill_color=color, fill_opacity=0.5, weight=1.5,
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=f"{row['City']} · {row['Risk']} · {int(row['Count']):,} accidents",
    ).add_to(m)

st_folium(m, width="100%", height=520, returned_objects=[])

# ── Table ─────────────────────────────────────────────────────────────────────
section_label("Top hotspots", t["accent"])
cols = ["City", "Cluster", "Risk", "Count", "Mean_Severity", "Peak_Hour", "Weather"]
top  = (filtered[cols].sort_values("Count", ascending=False)
        .head(15).reset_index(drop=True))
top["Count"]     = top["Count"].apply(lambda x: f"{int(x):,}")
top["Peak_Hour"] = top["Peak_Hour"].apply(lambda x: f"{int(x):02d}:00")
st.dataframe(top, use_container_width=True, hide_index=True)

footer()