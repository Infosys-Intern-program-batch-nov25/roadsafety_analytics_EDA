🚦 Road Safety Analytics – Exploratory Data Analysis (EDA)

An interactive Streamlit-based data analysis dashboard for exploring large-scale road accident data.
This project performs structured Exploratory Data Analysis (EDA) to uncover patterns, trends, and risk factors contributing to road accidents.

📌 Project Objectives

Perform exploratory analysis on road accident data

Analyze accident severity and distribution across key variables

Conduct univariate and bivariate statistical analysis

Visualize spatial accident patterns using geospatial plots

Present insights through an interactive Streamlit dashboard

📂 Project Structure
Project/
│── app.py                     # Main Streamlit application
│── requirements.txt           # Project dependencies
│
├── data/
│   └── US_Accidents_preprocessed.csv
│
├── modules/
│   ├── Home.py
│   ├── Preprocessing.py
│   ├── Univariate_Analysis.py
│   ├── Comparative_Analysis.py
│   ├── Geospatial_Analysis.py
│   ├── Insights_and_Hypothesis.py
│   └── Key_Findings.py
│
├── docs/
│   └── docs.txt               # Project documentation

🗂 Dataset Information

Dataset: US Road Accidents Dataset (preprocessed)

Type: Large-scale tabular dataset

Key Attributes:

Accident severity

Time and date features

Weather and visibility conditions

Road characteristics

Geographical coordinates

Distance affected by accidents

🧰 Tools & Technologies Used

Python

Streamlit – interactive dashboard

Pandas & NumPy – data processing

Matplotlib & Seaborn – statistical visualization

Plotly – interactive plots

Scikit-learn – basic modeling and preprocessing

SciPy – statistical analysis

🚀 How to Run the Project (Step-by-Step)
✅ Step 1: Clone or Download the Repository

Using Git:

git clone https://github.com/<your-username>/roadsafety_analytics_EDA.git


Or download the ZIP from GitHub and extract it.

✅ Step 2: Open the Project in VS Code

Open only the Project/ folder in VS Code:

roadsafety_analytics_EDA-main/Project

✅ Step 3: Create a Virtual Environment (Recommended)
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


macOS / Linux

source venv/bin/activate

✅ Step 4: Install Dependencies
pip install -r requirements.txt

✅ Step 5: Verify Dataset Placement

Ensure your CSV file is placed inside:

Project/data/US_Accidents_preprocessed.csv


The code uses relative paths, so no changes are required.

✅ Step 6: Run the Streamlit App

From inside the Project/ directory:

streamlit run app.py


Open your browser and navigate to:

http://localhost:8501

📊 Features of the Dashboard

Dataset overview and basic statistics

Univariate analysis with histograms and KDE plots

Bivariate and comparative analysis

Geospatial visualization of accident locations

Hypothesis formulation and insights

Summary of key findings

📈 Key Insights (Example)

Most accidents affect very short road distances

Accident distance distribution is highly right-skewed

Certain weather and visibility conditions correlate with higher severity

Spatial clustering observed in urban and highway regions

📝 Notes

The project follows a modular architecture for maintainability

Visualization parameters are tuned to handle large-scale skewed data

Median-based statistics are preferred where outliers exist

👨‍💻 Author

Nirupam Mondal
Data Analysis Internship Project
Streamlit | Python | EDA

📜 License

This project is for academic and internship evaluation purposes.
