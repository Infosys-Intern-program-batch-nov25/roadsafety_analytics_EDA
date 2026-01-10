🚦 Road Safety Analytics – Exploratory Data Analysis (EDA)

An interactive Streamlit-based data analysis dashboard designed to explore large-scale road accident data and extract meaningful insights related to road safety.

🎯 Project Objectives

Perform exploratory data analysis (EDA) on road accident data

Analyze accident severity and distribution across key variables

Conduct univariate and bivariate analysis

Visualize spatial accident patterns using geospatial plots

Present insights through an interactive Streamlit dashboard

📁 Project Structure

Project/

app.py – Main Streamlit application

requirements.txt – Project dependencies

data/

US_Accidents_preprocessed.csv – Preprocessed accident dataset

modules/

Home.py – Project overview and dataset information

Preprocessing.py – Data cleaning and preprocessing

Univariate_Analysis.py – Univariate statistical analysis

Comparative_Analysis.py – Bivariate and comparative analysis

Geospatial_Analysis.py – Spatial visualization of accidents

Insights_and_Hypothesis.py – Hypothesis formulation and insights

Key_Findings.py – Summary of key results

docs/

docs.txt – Project documentation

📊 Dataset Information

Dataset: US Road Accidents Dataset (Preprocessed)

Type: Large-scale tabular dataset

Key Attributes

Accident severity

Time and date features

Weather and visibility conditions

Road characteristics

Geographic coordinates

Distance affected by accidents

🧰 Tools & Technologies

Python

Streamlit

Pandas, NumPy

Matplotlib, Seaborn

Plotly

Scikit-learn

SciPy

🚀 How to Run the Project
Step 1: Clone the Repository
git clone https://github.com/<your-username>/roadsafety_analytics_EDA.git

Step 2: Navigate to the Project Folder
cd roadsafety_analytics_EDA/Project

Step 3: Create and Activate Virtual Environment
python -m venv venv


Windows

venv\Scripts\activate


macOS / Linux

source venv/bin/activate

Step 4: Install Dependencies
pip install -r requirements.txt

Step 5: Run the Streamlit App
streamlit run app.py


Open your browser and go to:
http://localhost:8501

📌 Key Insights (Summary)

Most accidents affect very short road distances

Distance distribution is highly right-skewed

Weather and visibility conditions influence accident severity

Spatial clustering is observed in urban and highway regions

👨‍💻 Author

Nirupam Mondal
Data Analysis Internship Project

📜 License

This project is intended for academic and internship evaluation purposes.
