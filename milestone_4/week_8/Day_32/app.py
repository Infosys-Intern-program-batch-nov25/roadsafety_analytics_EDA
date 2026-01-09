import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk

st.set_page_config(
    page_title="US Accidents Dashboard",
    layout="wide"
)

st.title("🚦 US Accidents Analysis Dashboard")
st.markdown("""
This dashboard is built using a **1 Million record sample** from the US Accidents dataset.

This Dashboard displays three types of analysis

1.Univariate Analysis

2.Bivariate Analysis

3.Geospatial Analysis

Use the sidebar to navigate between analysis pages.
""")


# SAMPLE DATASET LOAD
@st.cache_data
def load_data():
    return pd.read_csv("data/us_accidents_1M.csv", low_memory=False)

df = load_data()


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dataset Information",
        "Univariate Analysis",
        "Bivariate Analysis",
        "Geospatial Analysis"
    ]
)


# PAGE 1: DATASET INFORMATION
if page == "Dataset Information":
    st.title("📊 Dataset Information")

    st.subheader("Dataset Shape")
    st.write(df.shape)

    st.subheader("Column Data Types")
    st.write(df.dtypes)

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    st.subheader("Statistical Summary")
    st.write(df.describe())

# PAGE 2: UNIVARIATE ANALYSIS

elif page == "Univariate Analysis":
    st.title("📈 Univariate Analysis")

    column = st.selectbox(
        "Select a column",
        ['Severity', 'Temperature(F)', 'Visibility(mi)', 'Wind_Speed(mph)']
    )

    fig, ax = plt.subplots()
    sns.histplot(df[column].dropna(), kde=True, ax=ax)
    ax.set_title(f"Distribution of {column}")
    st.pyplot(fig)

# PAGE 3: BIVARIATE ANALYSIS

elif page == "Bivariate Analysis":
    st.title("📉 Bivariate Analysis")

    x_col = st.selectbox(
        "Select Weather Variable",
        ['Temperature(F)', 'Visibility(mi)', 'Wind_Speed(mph)']
    )

    fig, ax = plt.subplots()
    sns.boxplot(x=df['Severity'], y=df[x_col], ax=ax)
    ax.set_xlabel("Severity")
    ax.set_ylabel(x_col)
    st.pyplot(fig)


# PAGE 4: GEOSPATIAL ANALYSIS

elif page == "Geospatial Analysis":
    st.title("🗺️ Geospatial Analysis")

    geo_df = df[['Start_Lat', 'Start_Lng']].dropna()

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            initial_view_state=pdk.ViewState(
                latitude=geo_df['Start_Lat'].mean(),
                longitude=geo_df['Start_Lng'].mean(),
                zoom=3,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=geo_df.sample(20000),
                    get_position='[Start_Lng, Start_Lat]',
                    get_radius=200,
                    get_color=[255, 0, 0],
                    pickable=True,
                )
            ],
        )
    )
