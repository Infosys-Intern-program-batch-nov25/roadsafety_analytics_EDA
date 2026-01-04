import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Page Config
st.set_page_config(
    page_title="US Accidents Analytics",
    page_icon="🌙",
    layout="wide"
)


# Load Data (New 1M Sample)
@st.cache_data
def load_data():
    df = pd.read_csv("US_Accidents_March23.csv")
    # 🔄 Different 1M sample (changed seed)
    return df.sample(n=1_000_000, random_state=2025)

df = load_data()

# Sidebar
st.sidebar.title("🌙 US Accidents Dashboard")
page = st.sidebar.radio(
    "Navigate",
    [
        "📄 Dataset Information",
        "📊 Univariate Analysis",
        "📈 Bivariate Analysis",
        "🗺️ Geospatial Analysis"
    ]
)

# Dataset Info
if page == "📄 Dataset Information":
    st.title("📄 Dataset Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Records Used", f"{df.shape[0]:,}")
    #c2.metric("Total Features", df.shape[1])
    c3.metric("Missing Values", int(df.isnull().sum().sum()))

    st.subheader("🔍 Sample Data's")
    st.dataframe(df.head(100), use_container_width=True)

# Univariate

elif page == "📊 Univariate Analysis":
    st.title("📊 Univariate Analysis")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    col = st.selectbox("Select Feature", numeric_cols)

    fig = px.histogram(
        df,
        x=col,
        nbins=50,
        title=f"Distribution of {col}",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)


# Bivariate

elif page == "📈 Bivariate Analysis":
    st.title("📈 Bivariate Analysis")

    x_col = st.selectbox("X Axis", df.select_dtypes(include=["int64", "float64"]).columns)
    y_col = st.selectbox("Y Axis", df.select_dtypes(include=["int64", "float64"]).columns)

    fig = px.scatter(
        df.sample(15_000),
        x=x_col,
        y=y_col,
        opacity=0.6,
        title=f"{x_col} vs {y_col}",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)


# Geospatial

elif page == "🗺️ Geospatial Analysis":
    st.title("🗺️ Accident Locations")

    geo_df = df[['Start_Lat', 'Start_Lng']].dropna().sample(25_000)

    m = folium.Map(
        location=[39.5, -98.35],
        zoom_start=4,
        tiles="CartoDB dark_matter"
    )

    for _, row in geo_df.iterrows():
        folium.CircleMarker(
            location=[row['Start_Lat'], row['Start_Lng']],
            radius=2,
            color="#38bdf8",
            fill=True,
            fill_opacity=0.4
        ).add_to(m)

    st_folium(m, width=1300, height=650)
