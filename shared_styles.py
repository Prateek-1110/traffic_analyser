import streamlit as st
import os

# ── Design tokens — light off-white theme ─────────────────────────────────────
TOKENS = dict(
    # Backgrounds
    bg        = "#F7F6F2",      # off-white page bg
    bg2       = "#FFFFFF",      # card / panel white
    bg3       = "#EEECEA",      # subtle tinted surface
    bg4       = "#E5E3DF",      # input bg / divider

    # Borders
    border    = "#DDDBD6",
    border_h  = "#BFBDB8",

    # Text
    text      = "#1A1917",      # near-black body
    text_h    = "#0D0C0B",      # headings
    text_m    = "#5C5955",      # secondary / muted
    text_dim  = "#9E9B97",      # placeholder / dim

    # Accent palette
    accent    = "#1D6F4E",      # deep forest green (primary CTA)
    accent_lt = "#E8F5EE",      # green tint surface
    accent2   = "#2952A3",      # indigo (insights)
    accent2_lt= "#EBF0FB",
    accent3   = "#C2601A",      # amber-orange (risk)
    accent3_lt= "#FDF0E6",
    danger    = "#B91C1C",
    danger_lt = "#FEE2E2",

    # Chart
    chart_grid= "#E8E6E1",
    bar_dim   = "#D4D1CB",

    # Risk cards
    card_high = "#FEE2E2",
    card_med  = "#FEF3C7",
    card_low  = "#D1FAE5",

    # Navbar
    nav_bg    = "#FFFFFF",
    nav_border= "#E5E3DF",

    # Button text on accent bg
    btn_text  = "#FFFFFF",
)


def tokens():
    return TOKENS


def _current_page():
    """Return the base filename of the running script (without .py)."""
    try:
        import __main__
        script = getattr(__main__, "__file__", "") or ""
        return os.path.splitext(os.path.basename(script))[0]
    except Exception:
        return ""


def inject_styles():
    t = TOKENS
    page = _current_page()

    # ── CSS ──────────────────────────────────────────────────────────────────
    st.markdown(f"""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Reset ── */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {{
    background: {t['bg']} !important;
    color: {t['text']} !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}}

/* ── Hide Streamlit chrome ── */
[data-testid="stHeader"]         {{ display: none !important; }}
[data-testid="stToolbar"]        {{ display: none !important; }}
[data-testid="stDecoration"]     {{ display: none !important; }}
footer                           {{ display: none !important; }}

/* ── Hide native sidebar + toggle — we have a top nav ── */
[data-testid="stSidebar"]        {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}

/* ── Content sits below fixed navbar ── */
.block-container {{
    padding: 80px 2.5rem 3rem !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}}

/* ══════════════════════════════════════════
   TOP NAVBAR
   ══════════════════════════════════════════ */
.tha-nav {{
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    background: {t['nav_bg']};
    border-bottom: 1px solid {t['nav_border']};
    box-shadow: 0 1px 8px rgba(0,0,0,.07);
    height: 58px;
    display: flex;
    align-items: center;
    padding: 0 2.5rem;
}}
.tha-nav-brand {{
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 800;
    color: {t['accent']};
    text-decoration: none;
    letter-spacing: -.025em;
    margin-right: auto;
    display: flex;
    align-items: center;
    gap: 7px;
    white-space: nowrap;
}}
.tha-nav-brand .sub {{
    font-weight: 400;
    color: {t['text_dim']};
    font-size: 12px;
    letter-spacing: 0;
}}
.tha-nav-links {{
    display: flex;
    align-items: center;
    gap: 2px;
    list-style: none;
    margin: 0; padding: 0;
}}
.tha-nav-links li a {{
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 500;
    color: {t['text_m']};
    text-decoration: none;
    padding: 6px 13px;
    border-radius: 8px;
    transition: background .14s, color .14s;
    display: flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
}}
.tha-nav-links li a:hover {{
    background: {t['bg3']};
    color: {t['text']};
}}
.tha-nav-links li a.active {{
    background: {t['accent_lt']};
    color: {t['accent']};
    font-weight: 600;
}}
.tha-nav-divider {{
    width: 1px;
    height: 20px;
    background: {t['nav_border']};
    margin: 0 6px;
}}

/* ══════════════════════════════════════════
   TYPOGRAPHY
   ══════════════════════════════════════════ */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Inter', sans-serif !important;
    color: {t['text_h']} !important;
    letter-spacing: -.025em !important;
    line-height: 1.15 !important;
}}

/* ══════════════════════════════════════════
   METRICS
   ══════════════════════════════════════════ */
[data-testid="metric-container"] {{
    background: {t['bg2']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.3rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,.05) !important;
    transition: box-shadow .2s, transform .2s !important;
}}
[data-testid="metric-container"]:hover {{
    box-shadow: 0 6px 20px rgba(0,0,0,.09) !important;
    transform: translateY(-2px) !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Inter', sans-serif !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    color: {t['accent']} !important;
    letter-spacing: -.025em !important;
}}
[data-testid="stMetricLabel"] {{
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: .07em !important;
    text-transform: uppercase !important;
    color: {t['text_m']} !important;
}}

/* ══════════════════════════════════════════
   BUTTONS
   ══════════════════════════════════════════ */
[data-testid="baseButton-primary"] {{
    background: {t['accent']} !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 4px rgba(29,111,78,.3) !important;
    transition: opacity .18s, transform .15s, box-shadow .18s !important;
    min-height: 44px !important;
}}
[data-testid="baseButton-primary"]:hover {{
    opacity: .9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(29,111,78,.35) !important;
}}
[data-testid="baseButton-secondary"] {{
    background: {t['bg2']} !important;
    color: {t['text']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    min-height: 44px !important;
    transition: border-color .18s, background .18s !important;
}}
[data-testid="baseButton-secondary"]:hover {{
    border-color: {t['accent']} !important;
    background: {t['accent_lt']} !important;
    color: {t['accent']} !important;
}}

/* ══════════════════════════════════════════
   INPUTS
   ══════════════════════════════════════════ */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {{
    background: {t['bg2']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 8px !important;
    color: {t['text']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}}
[data-testid="stSelectbox"] > div > div {{
    background: {t['bg2']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 8px !important;
    color: {t['text']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}}
[data-baseweb="slider"] [role="slider"] {{
    background: {t['accent']} !important;
    border-color: {t['accent']} !important;
}}
[data-testid="stCheckbox"] label {{
    color: {t['text_m']} !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}}

/* ══════════════════════════════════════════
   SURFACES
   ══════════════════════════════════════════ */
[data-testid="stExpander"] {{
    background: {t['bg2']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,.04) !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}
[data-testid="stAlert"] {{
    background: {t['accent2_lt']} !important;
    border: 1px solid #C5D2F0 !important;
    border-left: 3px solid {t['accent2']} !important;
    border-radius: 10px !important;
    color: {t['accent2']} !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
}}

/* ══════════════════════════════════════════
   MISC
   ══════════════════════════════════════════ */
hr {{
    border: none !important;
    border-top: 1px solid {t['border']} !important;
    margin: 24px 0 !important;
}}
[data-testid="stCaptionContainer"] p {{
    color: {t['text_dim']} !important;
    font-size: 12px !important;
    font-family: 'Inter', sans-serif !important;
}}
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {t['bg3']}; }}
::-webkit-scrollbar-thumb {{ background: {t['border_h']}; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: {t['text_dim']}; }}

/* ══════════════════════════════════════════
   RESPONSIVE
   ══════════════════════════════════════════ */
@media (max-width: 900px) {{
    .block-container {{ padding: 70px 1.25rem 2rem !important; }}
    .tha-nav {{ padding: 0 1.25rem; }}
    .tha-nav-links li a {{ font-size: 12px; padding: 6px 9px; }}
    .tha-nav-divider {{ display: none; }}
}}
@media (max-width: 580px) {{
    .block-container {{ padding: 64px 0.75rem 2rem !important; }}
    .tha-nav {{ height: 52px; padding: 0 0.75rem; }}
    .tha-nav-brand .sub {{ display: none; }}
    .tha-nav-links li a {{ font-size: 11px; padding: 5px 7px; gap: 3px; }}
    [data-testid="stMetricValue"] {{ font-size: 1.3rem !important; }}
    [data-testid="baseButton-primary"] {{ min-height: 48px !important; }}
}}
</style>
""", unsafe_allow_html=True)

    # ── Top navbar HTML ───────────────────────────────────────────────────────
    pages = [
        ("🏠", "Home",       "app"),
        ("🗺", "Map",        "map"),
        ("📊", "Insights",   "insight"),
        ("🔮", "Risk Check", "risk_check"),
    ]

    items_html = ""
    for i, (icon, label, key) in enumerate(pages):
        active = "active" if page == key else ""
        # Streamlit multipage: pages live at /<PageFileName> relative to root
        href = "/" if key == "app" else f"/{key}"
        items_html += f'<li><a href="{href}" class="{active}">{icon} {label}</a></li>'
        if i == 0:
            items_html += '<div class="tha-nav-divider"></div>'

    st.markdown(f"""
<nav class="tha-nav">
    <a class="tha-nav-brand" href="/">
        🔺 TrafficLens <span class="sub">&nbsp;·&nbsp; Hotspot Analyzer</span>
    </a>
    <ul class="tha-nav-links">
        {items_html}
    </ul>
</nav>
""", unsafe_allow_html=True)


# ── Page header ───────────────────────────────────────────────────────────────
def page_header(tag, title, subtitle, color=None):
    t = TOKENS
    c = color or t['accent']
    st.markdown(f"""
<div style="padding:0.25rem 0 1.75rem">
    <p style="font-family:'JetBrains Mono',monospace;font-size:10px;
              letter-spacing:.2em;color:{c};text-transform:uppercase;
              margin:0 0 10px;font-weight:500">{tag}</p>
    <h1 style="font-family:'Inter',sans-serif;
               font-size:clamp(1.8rem,4vw,2.5rem);font-weight:800;
               color:{t['text_h']};margin:0 0 10px;
               letter-spacing:-.03em;line-height:1.1">{title}</h1>
    <p style="font-size:15px;color:{t['text_m']};margin:0;
              max-width:580px;line-height:1.7">{subtitle}</p>
    <div style="width:36px;height:3px;background:{c};
                border-radius:99px;margin-top:18px"></div>
</div>""", unsafe_allow_html=True)


# ── Section label ─────────────────────────────────────────────────────────────
def section_label(label, color=None):
    t = TOKENS
    c = color or t['accent']
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;margin:28px 0 14px">
    <div style="width:3px;height:16px;background:{c};border-radius:2px;flex-shrink:0"></div>
    <span style="font-family:'Inter',sans-serif;font-size:11px;font-weight:700;
                 letter-spacing:.1em;color:{c};text-transform:uppercase">{label}</span>
</div>""", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
def footer():
    t = TOKENS
    st.markdown(f"""
<div style="border-top:1px solid {t['border']};padding-top:20px;margin-top:48px;
            display:flex;justify-content:space-between;align-items:center;
            flex-wrap:wrap;gap:10px">
    <span style="font-family:'Inter',sans-serif;font-size:12px;color:{t['text_dim']}">
        Traffic Hotspot Analyzer &nbsp;·&nbsp; 3M+ records
    </span>
    <span style="font-family:'Inter',sans-serif;font-size:12px;color:{t['text_dim']}">
        Made with ♥ by&nbsp;
        <a href="https://github.com/Prateek-1110/traffic-hotspot-analyzer"
           style="color:{t['accent']};text-decoration:none;font-weight:600">
            Prateek Agrahari
        </a>
        &nbsp;·&nbsp;
        <a href="https://www.linkedin.com/in/prateek1110/"
           style="color:{t['accent2']};text-decoration:none;font-weight:600">
            LinkedIn
        </a>
    </span>
</div>""", unsafe_allow_html=True)