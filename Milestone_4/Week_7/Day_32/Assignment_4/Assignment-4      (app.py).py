import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
import warnings

warnings.filterwarnings("ignore")

#
# Page config
st.set_page_config(
    page_title="🚦 US Accidents Dashboard",
    page_icon="🛣️",
    layout="wide"
)

# Title
st.markdown("### ***🚦 US Accidents Dashboard***")

# Load full dataset (1M rows)
@st.cache_data
def load_data():
    return pd.read_csv("US_Accidents_Sample.csv")

df = load_data()

# Sidebar navigation
page = st.sidebar.radio("👇 Select Your Analysis Type", [
    "Dataset Information",
    "Univariate Analysis",
    "Bivariate Analysis",
    "Geospatial Analysis"
])

# ****************************************************** #
# Part A:Dataset Information
# ****************************************************** #
if page == "Dataset Information":
    st.markdown("### 📋 US Accidents Dataset Information")
    st.write("#### Preview of Dataset ")   # safer preview
    st.write(df.head(100000))
    st.write("#### Dataset Shape")
    st.write(df.shape)
    st.write("#### Column Data Types")
    st.write(df.dtypes)
    st.write("#### Missing Values Summary")
    st.write(df.isnull().sum())

# ****************************************************** #
# Part B: Univariate Analysis
# ****************************************************** #
elif page == "Univariate Analysis":
    st.markdown("### 📊 Univariate Analysis of US Accidents")
    column = st.selectbox("Select a column", df.columns)
    st.write(f"### Distribution of {column}")

    if pd.api.types.is_numeric_dtype(df[column]):
        fig, ax = plt.subplots()
        df[column].hist(bins=50, ax=ax, color="skyblue", edgecolor="black")
        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:

        top_values = df[column].value_counts().head(100)
        st.bar_chart(top_values)
        fig, ax = plt.subplots()
        top_values.plot(kind="bar", ax=ax, color="lightgreen", edgecolor="black")
        ax.set_title(f"Top 100 values of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Count")
        st.pyplot(fig)

# ****************************************************** #
# Part C: Bivariate Analysis
# ****************************************************** #
elif page == "Bivariate Analysis":
    st.markdown("### 🔗 Bivariate Analysis of US Accidents")
    x, y = st.selectbox("Select x variable", df.columns), st.selectbox("Select y variable", df.columns)
    df_sample = df.sample(min(50000, len(df)), random_state=42)

    # Both numeric 
    if pd.api.types.is_numeric_dtype(df[x]) and pd.api.types.is_numeric_dtype(df[y]):
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=df_sample, x=x, y=y, alpha=0.7, color="#E48400", ax=ax)
        ax.set_title(f"{x} vs {y}", fontsize=10, fontweight='bold')
        st.pyplot(fig)

    #  X categorical, Y numeric 
    elif pd.api.types.is_numeric_dtype(df[y]):
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.violinplot(data=df_sample, x=x, y=y, palette="Set3", ax=ax, inner="quartile")
        ax.set_title(f"{y} by {x}", fontsize=14, fontweight='bold')
        st.pyplot(fig)

    # Both categorical → heatmap
    else:
        st.markdown("### 🟦 Heatmap for Categorical vs Categorical")
        cross_tab = pd.crosstab(df_sample[x], df_sample[y])
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.heatmap(cross_tab, cmap="YlGnBu", annot=True, fmt="d", ax=ax)
        ax.set_title(f"{x} vs {y}", fontsize=10, fontweight='bold')
        st.pyplot(fig)

# ****************************************************** #
# Part D: Geospatial Analysis
# ****************************************************** #
elif page == "Geospatial Analysis":
    st.markdown("### 🗺️ Geospatial Analysis of US Accidents")
    # Drop missing coordinates
    df_geo = df.dropna(subset=["Start_Lat", "Start_Lng"])
    df_sample = df_geo.sample(100000, random_state=42)

    # Scatterplot layer
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_sample,
        get_position=["Start_Lng", "Start_Lat"],
        get_color=[255, 0, 0, 160],  
        get_radius=60,
        opacity=0.6,
    )

    # Render map with global background
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11", 
        initial_view_state=pdk.ViewState(
            latitude=37.5,  
            longitude=-95.0,
            zoom=2.5,       
        ),
        layers=[scatter_layer]
    ))