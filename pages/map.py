import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="Hotspot Map", page_icon="🗺", layout="wide")

st.title("🗺 Accident Hotspot Map")
st.caption("DBSCAN clusters across top US cities — click any circle for details")

# ── Load data (hotspot_summary.csv is small, lives in repo) ──────────────────
@st.cache_data
def load_hotspots():
    return pd.read_csv("data/hotspot_summary.csv")

df = load_hotspots()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.header("Filters")
cities   = ["All"] + sorted(df["City"].unique().tolist())
city_sel = st.sidebar.selectbox("City", cities)
risk_sel = st.sidebar.multiselect(
    "Risk level",
    ["High", "Medium", "Low"],
    default=["High", "Medium", "Low"]
)

filtered = df.copy()
if city_sel != "All":
    filtered = filtered[filtered["City"] == city_sel]
filtered = filtered[filtered["Risk"].isin(risk_sel)]

# ── Stats ─────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total hotspots", len(filtered))
c2.metric("High risk",   int((filtered["Risk"] == "High").sum()))
c3.metric("Medium risk", int((filtered["Risk"] == "Medium").sum()))
c4.metric("Low risk",    int((filtered["Risk"] == "Low").sum()))
st.markdown("---")

# ── Build Folium map ──────────────────────────────────────────────────────────
RISK_COLORS = {"High": "#e63946", "Medium": "#f4a261", "Low": "#2a9d8f"}

center_lat = filtered["Lat"].mean() if len(filtered) else 37.8
center_lng = filtered["Lng"].mean() if len(filtered) else -96.0

m = folium.Map(
    location=[center_lat, center_lng],
    zoom_start=5 if city_sel == "All" else 11,
    tiles="CartoDB dark_matter",
)

if len(filtered) > 0:
    HeatMap(
        filtered[["Lat", "Lng", "Count"]].values.tolist(),
        min_opacity=0.3, radius=18, blur=12,
        gradient={0.3: "#457b9d", 0.6: "#f4a261", 1.0: "#e63946"},
    ).add_to(m)

for _, row in filtered.iterrows():
    if pd.isna(row["Lat"]) or pd.isna(row["Lng"]):
        continue
    color  = RISK_COLORS.get(row["Risk"], "#888")
    radius = 8 + min(row["Count"] / 30, 25)
    popup_html = (
        f"<div style='font-family:system-ui;font-size:13px;min-width:190px'>"
        f"<b style='color:{color}'>{row['Risk']} Risk Hotspot</b><br><br>"
        f"<b>City:</b> {row['City']}<br>"
        f"<b>Accidents:</b> {int(row['Count']):,}<br>"
        f"<b>Mean severity:</b> {row['Mean_Severity']}<br>"
        f"<b>Peak hour:</b> {str(int(row['Peak_Hour'])).zfill(2)}:00<br>"
        f"<b>Weather:</b> {row['Weather']}</div>"
    )
    folium.CircleMarker(
        location=[row["Lat"], row["Lng"]],
        radius=radius,
        color=color, fill=True, fill_color=color,
        fill_opacity=0.55, weight=1.5,
        popup=folium.Popup(popup_html, max_width=240),
        tooltip=f"{row['City']} — {row['Risk']} Risk ({int(row['Count']):,} accidents)",
    ).add_to(m)

st_folium(m, width="100%", height=560, returned_objects=[])

# ── Top hotspots table ────────────────────────────────────────────────────────
st.markdown("### Top hotspots")
display_cols = ["City", "Cluster", "Risk", "Count", "Mean_Severity", "Peak_Hour", "Weather"]
top = (
    filtered[display_cols]
    .sort_values("Count", ascending=False)
    .head(15)
    .reset_index(drop=True)
)
top["Count"]     = top["Count"].apply(lambda x: f"{int(x):,}")
top["Peak_Hour"] = top["Peak_Hour"].apply(lambda x: f"{int(x):02d}:00")
st.dataframe(top, use_container_width=True, hide_index=True)