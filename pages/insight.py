import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from huggingface_hub import hf_hub_download

st.set_page_config(page_title="Insights", page_icon="📊", layout="wide")

st.title("📊 Accident Insights")
st.caption("Patterns across time, weather, severity, and geography")

# ── Download parquet from Hugging Face (cached after first load) ──────────────
@st.cache_data(show_spinner="Downloading dataset from Hugging Face (~first load only)...")
def load_data():
    path = hf_hub_download(
        repo_id="Prateek-1110/traffic_analyser",
        filename="accidents_clean.parquet",
        repo_type="dataset",
    )
    return pd.read_parquet(
        path,
        columns=["Severity", "Hour", "DayOfWeek", "MonthName",
                 "WeatherGroup", "Season", "State", "City", "TimeOfDay"]
    )

df = load_data()

st.metric("Total records", f"{len(df):,}")
st.markdown("---")

# ── Plot config ───────────────────────────────────────────────────────────────
COLORS = ["#e63946", "#457b9d", "#2a9d8f", "#e9c46a",
          "#f4a261", "#7c6af5", "#06d6a0", "#ef476f"]

PLOT_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#c9cde0",
    font_size=12,
)

# ── Row 1: Hour + Day ─────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Accidents by hour")
    by_hour = df.groupby("Hour").size().reset_index(name="count")
    by_hour["color"] = by_hour["Hour"].apply(
        lambda h: "#e63946" if h in [7, 8, 17, 18, 19] else "#457b9d"
    )
    fig = go.Figure(go.Bar(
        x=by_hour["Hour"], y=by_hour["count"],
        marker_color=by_hour["color"],
        hovertemplate="Hour %{x}:00<br>%{y:,} accidents<extra></extra>"
    ))
    fig.update_layout(xaxis_title="Hour", yaxis_title="Count",
                      **PLOT_THEME, margin=dict(l=10,r=10,t=10,b=10))
    fig.update_xaxes(gridcolor="#2e3248")
    fig.update_yaxes(gridcolor="#2e3248")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Red = rush hours (7–8am, 5–7pm)")

with col2:
    st.markdown("#### Accidents by day of week")
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    by_day = df["DayOfWeek"].value_counts().reindex(day_order).reset_index()
    by_day.columns = ["day", "count"]
    by_day["color"] = by_day["day"].apply(
        lambda d: "#f4a261" if d in ["Saturday","Sunday"] else "#2a9d8f"
    )
    fig = go.Figure(go.Bar(
        x=by_day["day"], y=by_day["count"],
        marker_color=by_day["color"],
        hovertemplate="%{x}<br>%{y:,} accidents<extra></extra>"
    ))
    fig.update_layout(xaxis_title="", yaxis_title="Count",
                      **PLOT_THEME, margin=dict(l=10,r=10,t=10,b=10))
    fig.update_xaxes(gridcolor="#2e3248")
    fig.update_yaxes(gridcolor="#2e3248")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Orange = weekends")

st.markdown("---")

# ── Row 2: Severity + Weather ─────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Severity distribution")
    by_sev = df["Severity"].value_counts().sort_index().reset_index()
    by_sev.columns = ["severity", "count"]
    by_sev["label"] = by_sev["severity"].apply(lambda s: f"Severity {s}")
    fig = px.pie(
        by_sev, names="label", values="count",
        color_discrete_sequence=["#2a9d8f","#457b9d","#f4a261","#e63946"],
        hole=0.55,
    )
    fig.update_layout(**PLOT_THEME, margin=dict(l=10,r=10,t=10,b=10),
                      showlegend=True, legend=dict(font_color="#c9cde0"))
    fig.update_traces(textinfo="percent", textfont_color="#c9cde0")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown("#### Top weather conditions")
    by_wx = df["WeatherGroup"].value_counts().head(7).reset_index()
    by_wx.columns = ["weather", "count"]
    fig = px.bar(
        by_wx, x="count", y="weather", orientation="h",
        color="weather", color_discrete_sequence=COLORS,
    )
    fig.update_layout(**PLOT_THEME, margin=dict(l=10,r=10,t=10,b=10),
                      yaxis=dict(categoryorder="total ascending"), showlegend=False)
    fig.update_xaxes(gridcolor="#2e3248")
    fig.update_yaxes(gridcolor="#2e3248")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Row 3: Heatmap ────────────────────────────────────────────────────────────
st.markdown("#### Accident density — hour × day of week")
pivot = df.groupby(["DayOfWeek","Hour"]).size().unstack(fill_value=0)
pivot = pivot.reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
fig = px.imshow(
    pivot,
    color_continuous_scale=["#1a1d27","#457b9d","#f4a261","#e63946"],
    labels=dict(x="Hour", y="", color="Accidents"),
    aspect="auto",
)
fig.update_layout(**PLOT_THEME, margin=dict(l=10,r=10,t=10,b=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Row 4: Top states ─────────────────────────────────────────────────────────
st.markdown("#### Top 10 states by accident count")
by_state = df["State"].value_counts().head(10).reset_index()
by_state.columns = ["state", "count"]
fig = px.bar(by_state, x="state", y="count",
             color_discrete_sequence=["#7c6af5"])
fig.update_layout(**PLOT_THEME, margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
fig.update_xaxes(gridcolor="#2e3248")
fig.update_yaxes(gridcolor="#2e3248")
st.plotly_chart(fig, use_container_width=True)