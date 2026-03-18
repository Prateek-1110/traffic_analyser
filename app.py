import streamlit as st

st.set_page_config(
    page_title="Traffic Hotspot Analyzer",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔺 Traffic Accident Hotspot Analyzer")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Records analyzed", "3M+")
col2.metric("Clustering", "DBSCAN")
col3.metric("Predictor", "Random Forest")
col4.metric("States covered", "49")

st.markdown("""
### What this project does

This dashboard analyzes **3 million+ US road accident records** to answer three questions:

- **Where** are accidents clustering? → Geospatial hotspot detection via DBSCAN
- **When and why** do they happen? → EDA across time, weather, and road features
- **How risky** is a specific location right now? → ML risk prediction (High / Medium / Low)

---

### Navigate using the sidebar

| Page | What it shows |
|---|---|
| 🗺 Map | Interactive hotspot map — click any cluster for details |
| 📊 Insights | Charts — accidents by hour, day, weather, severity, state |
| 🔮 Risk Check | Enter any location + time + weather → get predicted risk level |

---

**Dataset:** [US Accidents 2016–2023](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) by Sobhan Moosavi
**Author:** [Prateek Agrahari](https://www.linkedin.com/in/prateek1110/)
**Code:** [GitHub](https://github.com/Prateek-1110/traffic-hotspot-analyzer)
""")