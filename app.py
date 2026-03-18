import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared_styles import init_theme, inject_styles, tokens, footer, theme_toggle, page_header

st.set_page_config(
    page_title="Traffic Hotspot Analyzer",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_theme()
inject_styles()
t = tokens()

# ── Sidebar ───────────────────────────────────────────────────────────────────
# theme_toggle()
st.sidebar.markdown(f"""
<div style="padding:.5rem 0;font-size:12px;color:{t['text_m']};line-height:1.8">
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                letter-spacing:.18em;color:{t['accent']};
                text-transform:uppercase;margin-bottom:8px">About</div>
    End-to-end pipeline on 3M+ accident records.<br>
    DBSCAN clustering · Random Forest risk prediction.
    <br><br>
    <a href="https://www.linkedin.com/in/prateek1110/"
       style="color:{t['accent']};text-decoration:none;
              font-family:'JetBrains Mono',monospace;font-size:11px">
        linkedin/prateek1110
    </a>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding:2rem 0 1.5rem">
    <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                letter-spacing:.2em;color:{t['accent']};
                text-transform:uppercase;margin-bottom:14px">
        // data analytics project
    </div>
    <h1 style="font-family:'Syne',sans-serif;
               font-size:clamp(2rem,5vw,3.2rem);
               font-weight:800;color:{t['text_h']};
               line-height:1.08;margin:0 0 16px;letter-spacing:-.02em">
        Traffic Accident<br>
        <span style="color:{t['accent']}">Hotspot</span> Analyzer
    </h1>
    <p style="font-size:15px;color:{t['text_m']};
              max-width:540px;line-height:1.75;margin:0">
        3M+ US road accident records processed through a geospatial
        clustering and machine learning pipeline — surfaced as an
        interactive dashboard.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Records",   "3M+")
c2.metric("Algorithm", "DBSCAN")
c3.metric("Model",     "Random Forest")
c4.metric("States",    "49")
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(3,1fr);
            gap:16px;margin:8px 0 28px">
    <div style="background:{t['bg2']};border:1px solid {t['border']};
                border-top:2px solid {t['accent']};
                border-radius:12px;padding:22px 20px">
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                    color:{t['accent']};letter-spacing:.15em;margin-bottom:10px">
            01 / WHERE
        </div>
        <div style="font-size:15px;font-weight:600;
                    color:{t['text_h']};margin-bottom:8px">Hotspot detection</div>
        <div style="font-size:13px;color:{t['text_m']};line-height:1.7">
            DBSCAN clustering with haversine distance groups accidents into
            spatial hotspots, each profiled by severity, peak hour, and weather.
        </div>
    </div>
    <div style="background:{t['bg2']};border:1px solid {t['border']};
                border-top:2px solid {t['accent2']};
                border-radius:12px;padding:22px 20px">
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                    color:{t['accent2']};letter-spacing:.15em;margin-bottom:10px">
            02 / WHEN &amp; WHY
        </div>
        <div style="font-size:15px;font-weight:600;
                    color:{t['text_h']};margin-bottom:8px">Pattern analysis</div>
        <div style="font-size:13px;color:{t['text_m']};line-height:1.7">
            EDA across time of day, day of week, season, weather, and road
            infrastructure — reveals when and where risk is highest.
        </div>
    </div>
    <div style="background:{t['bg2']};border:1px solid {t['border']};
                border-top:2px solid {t['accent3']};
                border-radius:12px;padding:22px 20px">
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                    color:{t['accent3']};letter-spacing:.15em;margin-bottom:10px">
            03 / HOW RISKY
        </div>
        <div style="font-size:15px;font-weight:600;
                    color:{t['text_h']};margin-bottom:8px">Risk prediction</div>
        <div style="font-size:13px;color:{t['text_m']};line-height:1.7">
            Random Forest classifier predicts High / Medium / Low accident
            risk from any location, time, and weather condition.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Nav hint ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{t['bg2']};border:1px solid {t['border']};
            border-radius:10px;padding:16px 20px;
            display:flex;gap:32px;flex-wrap:wrap">
    <div>
        <span style="font-family:'JetBrains Mono',monospace;
                     font-size:11px;color:{t['accent']}">→ Map</span>
        <span style="font-size:12px;color:{t['text_m']};margin-left:10px">
            Interactive hotspot map with cluster details
        </span>
    </div>
    <div>
        <span style="font-family:'JetBrains Mono',monospace;
                     font-size:11px;color:{t['accent2']}">→ Insights</span>
        <span style="font-size:12px;color:{t['text_m']};margin-left:10px">
            Charts across time, weather, severity, geography
        </span>
    </div>
    <div>
        <span style="font-family:'JetBrains Mono',monospace;
                     font-size:11px;color:{t['accent3']}">→ Risk Check</span>
        <span style="font-size:12px;color:{t['text_m']};margin-left:10px">
            Live prediction for any location + time + weather
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

footer()