import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

# D:\Python\Scripts>streamlit run D:\AishuPythonPrgms\1.py

# ------------------------------------------------
# App Config
# ------------------------------------------------
st.set_page_config(
    page_title="US Accidents Analytics Dashboard",
    layout="wide"
)

# ------------------------------------------------
# Load data
# ------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\AishuPythonPrgms\US_Accidents_sample.csv")
    df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors="coerce")
    df["Year"] = df["Start_Time"].dt.year
    return df

df = load_data()

# ------------------------------------------------
# Sidebar Filters
# ------------------------------------------------
st.sidebar.header("🔎 Filters")

state_filter = st.sidebar.multiselect(
    "State",
    sorted(df["State"].dropna().unique())
)

severity_filter = st.sidebar.multiselect(
    "Severity",
    sorted(df["Severity"].dropna().unique())
)

year_filter = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].dropna().unique())
)

weather_filter = st.sidebar.multiselect(
    "Weather Condition",
    sorted(df["Weather_Condition"].dropna().unique())
)

filtered_df = df.copy()

if state_filter:
    filtered_df = filtered_df[filtered_df["State"].isin(state_filter)]
if severity_filter:
    filtered_df = filtered_df[filtered_df["Severity"].isin(severity_filter)]
if year_filter:
    filtered_df = filtered_df[filtered_df["Year"].isin(year_filter)]
if weather_filter:
    filtered_df = filtered_df[filtered_df["Weather_Condition"].isin(weather_filter)]

# ------------------------------------------------
# Navigation
# ------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "Dataset Information",
        "Univariate Analysis",
        "Bivariate Analysis",
        "Time Series Analysis",
        "Geospatial Analysis",
        "Correlation Analysis"
    ]
)

# =================================================
# PAGE 1: Dataset Information
# =================================================
if page == "Dataset Information":
    st.title("📊 Dataset Information")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", f"{filtered_df.shape[0]:,}")
    col2.metric("Columns", filtered_df.shape[1])
    col3.metric("Missing Values", f"{filtered_df.isna().sum().sum():,}")

    st.subheader("Data Sample")
    st.dataframe(filtered_df.head(20))

    st.subheader("Missing Values (%)")
    missing = (filtered_df.isna().mean() * 100).sort_values(ascending=False)
    st.dataframe(missing.to_frame("Missing %"))

# =================================================
# PAGE 2: Univariate Analysis
# =================================================
elif page == "Univariate Analysis":
    st.title("📈 Univariate Analysis")

    numeric_cols = filtered_df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = filtered_df.select_dtypes(include="object").columns.tolist()

    col = st.selectbox("Select column", numeric_cols + cat_cols)

    if col in numeric_cols:
        fig = px.histogram(filtered_df, x=col, nbins=50)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(filtered_df[col].describe())

    else:
        vc = filtered_df[col].value_counts().head(20)
        fig = px.bar(vc, x=vc.index, y=vc.values)
        st.plotly_chart(fig, use_container_width=True)

# =================================================
# PAGE 3: Bivariate Analysis
# =================================================
elif page == "Bivariate Analysis":
    st.title("🔗 Bivariate Analysis")

    numeric_cols = filtered_df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = filtered_df.select_dtypes(include="object").columns.tolist()

    analysis = st.radio("Analysis Type", ["Numeric vs Numeric", "Categorical vs Numeric"])

    if analysis == "Numeric vs Numeric":
        x = st.selectbox("X", numeric_cols)
        y = st.selectbox("Y", numeric_cols, index=1)
        fig = px.scatter(
            filtered_df.sample(min(50_000, len(filtered_df))),
            x=x,
            y=y,
            opacity=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        cat = st.selectbox("Category", cat_cols)
        num = st.selectbox("Numeric", numeric_cols)
        fig = px.box(
            filtered_df.sample(min(100_000, len(filtered_df))),
            x=cat,
            y=num
        )
        st.plotly_chart(fig, use_container_width=True)

# =================================================
# PAGE 4: Time Series Analysis
# =================================================
elif page == "Time Series Analysis":
    st.title("⏱️ Time Series Analysis")

    time_df = filtered_df.dropna(subset=["Start_Time"])
    time_series = (
        time_df
        .groupby(time_df["Start_Time"].dt.to_period("M"))
        .size()
        .reset_index(name="Accidents")
    )
    time_series["Start_Time"] = time_series["Start_Time"].astype(str)

    fig = px.line(
        time_series,
        x="Start_Time",
        y="Accidents",
        title="Monthly Accident Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# PAGE 5: Geospatial Analysis
# =================================================
elif page == "Geospatial Analysis":
    st.title("🗺️ Geospatial Analysis")

    geo_df = filtered_df[["Start_Lat", "Start_Lng", "Severity"]].dropna()
    geo_df = geo_df.sample(min(50_000, len(geo_df)))

    fig = px.scatter_mapbox(
        geo_df,
        lat="Start_Lat",
        lon="Start_Lng",
        color="Severity",
        zoom=3,
        height=600
    )
    fig.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔥 Accident Hotspots (DBSCAN)")
    coords = geo_df[["Start_Lat", "Start_Lng"]].values
    db = DBSCAN(eps=0.05, min_samples=50).fit(coords)
    geo_df["Cluster"] = db.labels_

    hotspot_df = geo_df[geo_df["Cluster"] != -1]
    fig2 = px.scatter_mapbox(
        hotspot_df,
        lat="Start_Lat",
        lon="Start_Lng",
        color="Cluster",
        zoom=3,
        height=600
    )
    fig2.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig2, use_container_width=True)

# =================================================
# PAGE 6: Correlation Analysis
# =================================================
elif page == "Correlation Analysis":
    st.title("📌 Correlation Analysis")

    numeric_df = filtered_df.select_dtypes(include=np.number)
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
