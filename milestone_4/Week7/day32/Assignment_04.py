import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="US Accidents Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Load dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    """
    Load the preprocessed 1M sampled accident dataset
    """
    return pd.read_csv("accidents_1M.csv")

df = load_data()

# --------------------------------------------------
# App title
# --------------------------------------------------
st.title("US Road Accidents Analysis Dashboard")

# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Select Analysis Page",
    (
        "Dataset Information",
        "Univariate Analysis",
        "Bivariate Analysis",
        "Geospatial Analysis"
    )
)

# ==================================================
# PAGE A: Dataset Information
# ==================================================
if menu == "Dataset Information":
    st.header("Dataset Information")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Rows", df.shape[0])
    with col2:
        st.metric("Columns", df.shape[1])

    st.subheader("Column Names")
    st.write(df.columns.tolist())

    st.subheader("Missing Values (%)")
    missing = (df.isna().mean() * 100).round(2)
    st.dataframe(missing[missing > 0])

    st.subheader("Sample Records")
    st.dataframe(df.head())

# ==================================================
# PAGE B: Univariate Analysis
# ==================================================
elif menu == "Univariate Analysis":
    st.header("Univariate Analysis")

    # Severity distribution
    st.subheader("Accident Severity Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x="Severity", data=df, ax=ax)
    ax.set_xlabel("Severity Level")
    ax.set_ylabel("Number of Accidents")
    st.pyplot(fig)

    # Hour-wise distribution
    st.subheader("Accidents by Hour of Day")
    df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
    df['Hour'] = df['Start_Time'].dt.hour

    fig, ax = plt.subplots()
    sns.histplot(df['Hour'].dropna(), bins=24, ax=ax)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Accident Count")
    st.pyplot(fig)

    # Weather conditions
    st.subheader("Top 10 Weather Conditions")
    weather_counts = df['Weather_Condition'].value_counts().head(10)
    st.bar_chart(weather_counts)

# ==================================================
# PAGE C: Bivariate Analysis
# ==================================================
elif menu == "Bivariate Analysis":
    st.header("Bivariate Analysis")

    # Severity vs Sunrise/Sunset
    st.subheader("Severity vs Day/Night")
    fig, ax = plt.subplots()
    sns.countplot(
        x="Severity",
        hue="Sunrise_Sunset",
        data=df,
        ax=ax
    )
    ax.set_xlabel("Severity")
    ax.set_ylabel("Accident Count")
    st.pyplot(fig)

    # Severity vs Visibility
    st.subheader("Severity vs Visibility")
    fig, ax = plt.subplots()
    sns.boxplot(
        x="Severity",
        y="Visibility(mi)",
        data=df,
        ax=ax
    )
    ax.set_xlabel("Severity")
    ax.set_ylabel("Visibility (miles)")
    st.pyplot(fig)

    # Severity vs Weather (Top 5)
    st.subheader("Severity vs Weather Condition (Top 5)")
    top_weather = df['Weather_Condition'].value_counts().head(5).index
    filtered_df = df[df['Weather_Condition'].isin(top_weather)]

    fig, ax = plt.subplots()
    sns.countplot(
        x="Weather_Condition",
        hue="Severity",
        data=filtered_df,
        ax=ax
    )
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Accident Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ==================================================
# PAGE D: Geospatial Analysis
# ==================================================
elif menu == "Geospatial Analysis":
    st.header("Geospatial Analysis")

    st.write(
        "The map below visualizes accident locations using latitude and longitude. "
        "A subset of the dataset is used for better performance."
    )

    # Prepare data for mapping
    geo_df = df[['Start_Lat', 'Start_Lng']].dropna().sample(
        n=10000,
        random_state=42
    )

    # Rename columns as required by st.map
    geo_df = geo_df.rename(
        columns={
            'Start_Lat': 'lat',
            'Start_Lng': 'lon'
        }
    )

    # Display map
    st.map(geo_df)
