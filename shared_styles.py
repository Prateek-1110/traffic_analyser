import streamlit as st
DARK_TOKENS = dict(
    bg="#080b12", bg2="#0d1117", bg3="#141928",
    border="#2a3447", border_h="#435373",          
    text="#dce3f5", text_h="#ffffff",            
    text_m="#8898b5", text_dim="#526280",         
    accent="#4fffb0", accent2="#7c6af5", accent3="#f4a261", danger="#e63946",
    chart_grid="#1c2336", sidebar_bg="#0d1017",
    bar_dim="#25344a", btn_text="#080b12",
    card_high="#2a1417", card_med="#241910", card_low="#0c2418", 
)


def tokens():
    return DARK_TOKENS


def inject_styles():
    t = DARK_TOKENS

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Syne:wght@400;600;700;800&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {{
    background-color: {t['bg']} !important;
    color: {t['text']} !important;
    font-family: 'Syne', sans-serif !important;
}}

[data-testid="stHeader"] {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {t['sidebar_bg']} !important;
    border-right: 1px solid {t['border']} !important;
}}
[data-testid="stSidebar"] * {{
    font-family: 'Syne', sans-serif !important;
}}
[data-testid="stSidebarNav"] a {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    color: {t['text_m']} !important;
    transition: color .2s;
}}
[data-testid="stSidebarNav"] [aria-selected="true"],
[data-testid="stSidebarNav"] a:hover {{
    color: {t['accent']} !important;
}}

/* ── Sidebar toggle — always visible, always styled ── */
[data-testid="collapsedControl"] {{
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 0.6rem !important;
    left: 0.4rem !important;
    z-index: 99999 !important;
    background: {t['bg2']} !important;
    border: 1px solid {t['accent']} !important;
    border-radius: 8px !important;
    padding: 4px 10px !important;
    min-width: 80px !important;
    align-items: center !important;
    gap: 6px !important;
    cursor: pointer !important;
    box-shadow: 0 2px 10px rgba(0,0,0,.25) !important;
}}
[data-testid="collapsedControl"]::after {{
    content: "Expand" !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    color: {t['accent']} !important;
    letter-spacing: .06em !important;
}}
[data-testid="collapsedControl"] svg {{
    color: {t['accent']} !important;
    fill: {t['accent']} !important;
    width: 14px !important;
    height: 14px !important;
}}
[data-testid="collapsedControl"]:hover {{
    background: {t['bg3']} !important;
    border-color: {t['accent']} !important;
}}

/* ── Block container ── */
.block-container {{
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1240px;
}}

/* ── Metrics ── */
[data-testid="metric-container"] {{
    background: {t['bg2']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    transition: border-color .25s, transform .2s;
}}
[data-testid="metric-container"]:hover {{
    border-color: {t['accent']} !important;
    transform: translateY(-2px);
}}
[data-testid="stMetricValue"] {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.5rem !important;
    color: {t['accent']} !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: 10px !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    color: {t['text_m']} !important;
}}

/* ── Primary button ── */
[data-testid="baseButton-primary"] {{
    background: {t['accent']} !important;
    color: {t['btn_text']} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: .06em !important;
    border: none !important;
    border-radius: 8px !important;
    transition: opacity .2s, transform .15s !important;
}}
[data-testid="baseButton-primary"]:hover {{
    opacity: .88 !important;
    transform: translateY(-1px) !important;
}}

/* ── Secondary button ── */
[data-testid="baseButton-secondary"] {{
    background: {t['bg3']} !important;
    color: {t['text']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}}
[data-testid="baseButton-secondary"]:hover {{
    border-color: {t['accent']} !important;
    color: {t['accent']} !important;
}}

/* ── Inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {{
    background: {t['bg2']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 8px !important;
    color: {t['text']} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}}

/* ── Slider ── */
[data-baseweb="slider"] [role="slider"] {{
    background: {t['accent']} !important;
    border-color: {t['accent']} !important;
}}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label {{
    color: {t['text_m']} !important;
    font-size: 13px !important;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
    border: 1px solid {t['border']} !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background: {t['bg2']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 10px !important;
}}

/* ── Alert ── */
[data-testid="stAlert"] {{
    background: {t['bg2']} !important;
    border: 1px solid {t['border']} !important;
    border-left: 3px solid {t['accent2']} !important;
    border-radius: 10px !important;
    color: {t['text_m']} !important;
    font-size: 13px !important;
}}

hr {{ border-color: {t['border']} !important; }}

::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {t['bg']}; }}
::-webkit-scrollbar-thumb {{ background: {t['border']}; border-radius: 2px; }}
::-webkit-scrollbar-thumb:hover {{ background: {t['accent']}; }}
</style>
""", unsafe_allow_html=True)




def page_header(tag, title, subtitle, color=None):
    t = tokens()
    c = color or t['accent']
    st.markdown(f"""
<div style="padding:1.2rem 0 1rem">
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                letter-spacing:.2em;color:{c};text-transform:uppercase;
                margin-bottom:10px">{tag}</div>
    <h1 style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
               color:{t['text_h']};margin:0 0 6px;letter-spacing:-.02em">{title}</h1>
    <p style="font-size:13px;color:{t['text_m']};margin:0">{subtitle}</p>
</div>""", unsafe_allow_html=True)


def section_label(label, color=None):
    t = tokens()
    c = color or t['accent']
    st.markdown(f"""
<div style="font-family:'JetBrains Mono',monospace;font-size:10px;
            letter-spacing:.2em;color:{c};text-transform:uppercase;
            margin:24px 0 12px;padding-bottom:8px;
            border-bottom:1px solid {t['border']}">// {label}</div>
""", unsafe_allow_html=True)


def footer():
    t = tokens()
    st.markdown(f"""
<div style="border-top:1px solid {t['border']};padding-top:16px;margin-top:40px;
            display:flex;justify-content:flex-end;align-items:center">
    <span style="font-size:12px;color:{t['text_dim']}">
        Made with 🤍 &amp; ♥ by&nbsp;
        <a href="https://github.com/Prateek-1110/traffic-hotspot-analyzer"
           style="color:{t['accent']};text-decoration:none;
                  font-family:'JetBrains Mono',monospace;font-size:12px">
            Prateek Agrahari
        </a>
    </span>
</div>""", unsafe_allow_html=True)