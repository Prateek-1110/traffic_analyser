import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared_styles import inject_styles, tokens, footer

st.set_page_config(
    page_title="TrafficLens — Hotspot Analyzer",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
t = tokens()

# ── Hero ──────────────────────────────────────────────────────────────────────
hero_html = """
<div style="padding:1.5rem 0 2rem">
    <p style="font-family:'JetBrains Mono',monospace;font-size:10px;
              letter-spacing:.22em;color:COLOR_ACCENT;text-transform:uppercase;
              margin:0 0 14px;font-weight:500">// data analytics project</p>
    <h1 style="font-family:'Inter',sans-serif;
               font-size:clamp(2rem,5vw,3.4rem);font-weight:800;
               color:COLOR_TEXT_H;line-height:1.08;margin:0 0 18px;
               letter-spacing:-.035em">
        Traffic Accident<br>
        <span style="color:COLOR_ACCENT">Hotspot</span> Analyzer
    </h1>
    <p style="font-size:16px;color:COLOR_TEXT_M;max-width:520px;
              line-height:1.75;margin:0">
        3M+ US road accident records processed through a geospatial
        clustering and machine learning pipeline — surfaced as an
        interactive dashboard.
    </p>
</div>
"""

hero_html = (hero_html
    .replace("COLOR_ACCENT",  t["accent"])
    .replace("COLOR_TEXT_H",  t["text_h"])
    .replace("COLOR_TEXT_M",  t["text_m"])
)
st.markdown(hero_html, unsafe_allow_html=True)

# ── Stats row ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Records",   "3M+")
c2.metric("Algorithm", "DBSCAN")
c3.metric("Model",     "Random Forest")
c4.metric("States",    "49")

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────────
# Build each card as a plain string — no nested f-string interpolation
def feature_card(num, label, title, desc, color):
    return (
        "<div style='"
        "background:#FFFFFF;"
        "border:1px solid " + t["border"] + ";"
        "border-top:4px solid " + color + ";"
        "border-radius:16px;"
        "padding:24px 22px;"
        "box-shadow:0 1px 4px rgba(0,0,0,.05);"
        "flex:1;"
        "min-width:260px'>"
            "<p style='"
            "font-family:JetBrains Mono,monospace;"
            "font-size:10px;"
            "color:" + color + ";"
            "letter-spacing:.15em;"
            "text-transform:uppercase;"
            "margin:0 0 10px;"
            "font-weight:600'>" + num + " / " + label + "</p>"
            "<p style='"
            "font-size:16px;"
            "font-weight:800;"
            "color:" + t["text_h"] + ";"
            "margin:0 0 8px'>" + title + "</p>"
            "<p style='"
            "font-size:13px;"
            "color:" + t["text_m"] + ";"
            "line-height:1.65;"
            "margin:0'>" + desc + "</p>"
        "</div>"
    )

cards_html = (
    "<div style='display:flex;flex-wrap:wrap;gap:16px;margin-bottom:32px'>"
    + feature_card(
        "01", "WHERE", "Hotspot Detection",
        "DBSCAN clustering with haversine distance groups accidents into "
        "spatial hotspots, each profiled by severity, peak hour, and weather.",
        t["accent"]
    )
    + feature_card(
        "02", "WHEN &amp; WHY", "Pattern Analysis",
        "EDA across time of day, day of week, season, weather, and road "
        "infrastructure — reveals when and where risk is statistically highest.",
        t["accent2"]
    )
    + feature_card(
        "03", "HOW RISKY", "Risk Prediction",
        "Random Forest classifier predicts High / Medium / Low accident "
        "risk from any location, time, and weather condition.",
        t["accent3"]
    )
    + "</div>"
)

st.markdown(cards_html, unsafe_allow_html=True)

# ── Quick nav cards ───────────────────────────────────────────────────────────
def nav_card(href, icon, label, sublabel, color):
    return (
        "<a href='" + href + "' style='text-decoration:none;color:inherit'>"
        "<div style='"
        "background:" + t["bg2"] + ";"
        "border:1px solid " + t["border"] + ";"
        "border-radius:12px;"
        "padding:14px 20px;"
        "display:flex;"
        "align-items:center;"
        "gap:12px;"
        "transition:box-shadow .15s'>"
            "<span style='font-size:22px'>" + icon + "</span>"
            "<div>"
                "<div style='font-size:14px;font-weight:700;color:" + color + "'>" + label + "</div>"
                "<div style='font-size:11px;color:" + t["text_m"] + "'>" + sublabel + "</div>"
            "</div>"
        "</div>"
        "</a>"
    )

nav_html = (
    "<div style='"
    "background:" + t["bg3"] + ";"
    "border:1px solid " + t["border"] + ";"
    "border-radius:14px;"
    "padding:24px'>"
        "<p style='"
        "font-family:Inter,sans-serif;"
        "font-size:11px;"
        "font-weight:700;"
        "letter-spacing:.08em;"
        "text-transform:uppercase;"
        "color:" + t["text_dim"] + ";"
        "margin:0 0 16px'>Jump to Module</p>"
        "<div style='display:flex;flex-wrap:wrap;gap:14px'>"
        + nav_card("/map",        "🗺",  "Map View",   "Explore clusters",  t["accent"])
        + nav_card("/insight",    "📊",  "Analytics",  "Deep dive charts",  t["accent2"])
        + nav_card("/risk_check", "🔮",  "Risk Check", "Predict live risk", t["accent3"])
        + "</div>"
    "</div>"
)

st.markdown(nav_html, unsafe_allow_html=True)
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

footer()