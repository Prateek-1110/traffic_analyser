import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from huggingface_hub import hf_hub_download
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared_styles import (init_theme, inject_styles, tokens, footer,
                           theme_toggle, page_header, section_label)

st.set_page_config(page_title="Insights", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")
init_theme()
inject_styles()
t = tokens()

theme_toggle()

# ── Load ──────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Downloading dataset from Hugging Face…")
def load_data():
    path = hf_hub_download(
        repo_id="Prateek-1110/traffic_analyser",
        filename="accidents_clean.parquet",
        repo_type="dataset",
    )
    return pd.read_parquet(
        path, columns=["Severity", "Hour", "DayOfWeek", "MonthName",
                       "WeatherGroup", "Season", "State", "City", "TimeOfDay"]
    )

with st.spinner("Loading dataset…"):
    df = load_data()

page_header("// 02 · insights", "Accident Insights",
            "Patterns across time, weather, severity, and geography", t["accent2"])
st.metric("Total records", f"{len(df):,}")
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── Chart theme ───────────────────────────────────────────────────────────────
is_dark = st.session_state.get("theme", "dark") == "dark"
GRID    = dict(gridcolor=t["chart_grid"], zerolinecolor=t["chart_grid"])
FONT    = dict(family="JetBrains Mono, monospace", color=t["text_m"], size=11)
LAYOUT  = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
               font=FONT, margin=dict(l=8, r=8, t=32, b=8))
TITLE_F = dict(color=t["text_h"], size=13, family="Syne, sans-serif")
ACC     = [t["accent"], t["accent2"], t["accent3"], t["danger"],
           "#457b9d", "#2a9d8f", "#e9c46a", "#ef476f"]
DIM     = t["bar_dim"]

# ── Hour + Day ────────────────────────────────────────────────────────────────
section_label("Time patterns", t["accent"])
col1, col2 = st.columns(2)

with col1:
    by_hour = df.groupby("Hour").size().reset_index(name="count")
    by_hour["rush"] = by_hour["Hour"].isin([7, 8, 17, 18, 19])
    fig = go.Figure(go.Bar(
        x=by_hour["Hour"], y=by_hour["count"],
        marker_color=by_hour["rush"].map({True: t["accent"], False: DIM}),
        marker_line_width=0,
        hovertemplate="<b>%{x}:00</b><br>%{y:,} accidents<extra></extra>",
    ))
    fig.update_layout(title=dict(text="Accidents by hour", font=TITLE_F),
                      xaxis=dict(title="Hour", **GRID, tickfont=FONT),
                      yaxis=dict(**GRID, tickfont=FONT),
                      showlegend=False, **LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Highlighted = rush hours (7–8am, 5–7pm)")

with col2:
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    by_day = df["DayOfWeek"].value_counts().reindex(day_order).reset_index()
    by_day.columns = ["day", "count"]
    by_day["wknd"] = by_day["day"].isin(["Saturday", "Sunday"])
    fig = go.Figure(go.Bar(
        x=by_day["day"], y=by_day["count"],
        marker_color=by_day["wknd"].map({True: t["accent3"], False: DIM}),
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>",
    ))
    fig.update_layout(title=dict(text="Accidents by day of week", font=TITLE_F),
                      xaxis=dict(**GRID, tickfont=FONT),
                      yaxis=dict(**GRID, tickfont=FONT),
                      showlegend=False, **LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Highlighted = weekends")

# ── Heatmap ───────────────────────────────────────────────────────────────────
section_label("Hour × day density", t["accent2"])
pivot = (df.groupby(["DayOfWeek", "Hour"]).size().unstack(fill_value=0)
         .reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
cs = (["#080b12","#0d1a2e", t["accent2"], t["accent"]] if is_dark
      else ["#f4f5f9","#dde1ec", t["accent2"], t["accent"]])
fig = px.imshow(pivot, color_continuous_scale=cs,
                labels=dict(x="Hour", y="", color="Accidents"), aspect="auto")
fig.update_layout(title=dict(text="Accident density — hour × day", font=TITLE_F),
                  coloraxis_colorbar=dict(tickfont=FONT), **LAYOUT)
fig.update_xaxes(**GRID, tickfont=FONT)
fig.update_yaxes(gridcolor=t["chart_grid"], tickfont=FONT)
st.plotly_chart(fig, use_container_width=True)

# ── Severity + Weather ────────────────────────────────────────────────────────
section_label("Severity & weather", t["accent3"])
col3, col4 = st.columns(2)

with col3:
    by_sev = df["Severity"].value_counts().sort_index().reset_index()
    by_sev.columns = ["severity", "count"]
    by_sev["label"] = by_sev["severity"].apply(lambda s: f"Severity {int(s)}")
    fig = px.pie(by_sev, names="label", values="count", hole=0.62,
                 color_discrete_sequence=["#2a9d8f","#457b9d", t["accent3"], t["danger"]])
    fig.update_layout(title=dict(text="Severity distribution", font=TITLE_F),
                      showlegend=True,
                      legend=dict(font=dict(color=t["text_m"], size=11)),
                      **LAYOUT)
    fig.update_traces(textinfo="percent",
                      textfont=dict(color=t["text_h"], size=11))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    by_wx = df["WeatherGroup"].value_counts().head(7).reset_index()
    by_wx.columns = ["weather", "count"]
    fig = go.Figure(go.Bar(
        x=by_wx["count"], y=by_wx["weather"], orientation="h",
        marker_color=ACC[:len(by_wx)], marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>%{x:,}<extra></extra>",
    ))
    fig.update_layout(title=dict(text="Weather conditions", font=TITLE_F),
                      xaxis=dict(**GRID, tickfont=FONT),
                      yaxis=dict(categoryorder="total ascending",
                                 gridcolor=t["chart_grid"], tickfont=FONT),
                      showlegend=False, **LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

# ── States ────────────────────────────────────────────────────────────────────
section_label("Geography", t["danger"])
by_state = df["State"].value_counts().head(10).reset_index()
by_state.columns = ["state", "count"]
fig = go.Figure(go.Bar(
    x=by_state["state"], y=by_state["count"],
    marker=dict(
        color=by_state["count"],
        colorscale=[[0, DIM], [0.5, t["accent2"]], [1, t["accent"]]],
        showscale=False,
    ),
    marker_line_width=0,
    hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>",
))
fig.update_layout(title=dict(text="Top 10 states by accident count", font=TITLE_F),
                  xaxis=dict(**GRID, tickfont=FONT),
                  yaxis=dict(**GRID, tickfont=FONT),
                  showlegend=False, **LAYOUT)
st.plotly_chart(fig, use_container_width=True)

footer()