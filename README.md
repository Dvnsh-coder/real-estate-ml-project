# Machine Learning Based Buyer Segmentation and Investment Profiling for Real Estate Market Intelligence

## 📌 Project Overview

This project develops a machine learning-based buyer segmentation and investment profiling system for the real estate market.

The system combines client-level demographic, behavioral, financing, and property-related information to identify groups of buyers with similar characteristics. These segments can help support more targeted marketing, buyer understanding, and real estate investment analysis.

The project also includes an interactive Streamlit dashboard for exploring buyer segments, investment behavior, geographic patterns, and segment-level insights.

---

## 🎯 Problem Statement

Real estate buyers have different demographic characteristics, purchasing purposes, financing preferences, and property activity.

Without data-driven buyer segmentation, real estate organizations may face challenges such as:

- Generic marketing strategies
- Difficulty identifying different buyer profiles
- Limited understanding of investment behavior
- Inefficient targeting of potential buyers
- Difficulty analyzing geographic and financing patterns

This project addresses these challenges by applying unsupervised machine learning techniques to identify meaningful buyer profiles from real estate and client data.

---

## 🎯 Objectives

The main objectives of this project are:

- Clean and prepare real estate client and property data.
- Integrate client information with property transaction information.
- Engineer client-level behavioral and property-related features.
- Encode categorical variables and scale numerical features.
- Apply K-Means and Agglomerative Hierarchical Clustering.
- Evaluate clustering using the Elbow Method and Silhouette Score.
- Identify and interpret distinct buyer profiles.
- Analyze acquisition purpose, financing behavior, referral channels, demographics, and property activity.
- Develop an interactive Streamlit dashboard for buyer intelligence.
- Provide data-driven insights that can support real estate marketing and investment analysis.

---

## 📊 Datasets

The project uses two datasets.

### Client Dataset

The client dataset contains information about individual buyers and organizations, including:

- Client ID
- Client type
- Gender
- Country
- Region
- Date of birth
- Acquisition purpose
- Loan application status
- Referral channel
- Satisfaction score

### Property Dataset

The property dataset contains property transaction information, including:

- Listing ID
- Tower number
- Transaction date
- Unit category
- Unit number
- Floor area
- Sale price
- Listing status
- Client reference

The two datasets are connected using the client identifier and property client reference.

---

## 🔄 Project Methodology

### 1. Data Cleaning

The datasets were inspected for:

- Missing values
- Duplicate records
- Invalid client references
- Inconsistent data formats
- Incorrect data types

Property records without a recorded client reference were retained because they represent transactions where a client was not recorded rather than invalid client records.

Sale prices were converted from currency-formatted strings into numerical values, and transaction dates were converted into datetime format.

---

### 2. Feature Engineering

Client-level features were created by aggregating property information for each client.

The engineered features include:

- Property count
- Total property value
- Average property value
- Average floor area
- Age

These features provide additional information about buyer activity and property involvement.

> Note: Total property value and related property features represent observable property activity/value exposure. They are not treated as direct measures of client income or wealth because the dataset does not contain an income variable.

---

### 3. Feature Encoding

Categorical variables were converted into numerical features using One-Hot Encoding.

The final behavior-focused clustering features included:

- Gender
- Acquisition purpose
- Loan application status
- Referral channel
- Age
- Satisfaction score
- Property count
- Total property value
- Average property value
- Average floor area

Geographic variables and client type were excluded from the final clustering model after sensitivity analysis showed that they could dominate the clustering structure.

They were retained for segment profiling and dashboard analysis.

---

### 4. Feature Scaling

Numerical and encoded features were standardized using `StandardScaler`.

Scaling ensures that variables with larger numerical ranges do not disproportionately influence the clustering algorithm.

---

## 🤖 Machine Learning Approach

Two unsupervised clustering techniques were evaluated:

### K-Means Clustering

K-Means was evaluated across multiple cluster counts using the Elbow Method and Silhouette Score.

### Agglomerative Hierarchical Clustering

Agglomerative Hierarchical Clustering was also evaluated across multiple cluster counts.

The final model used:

**Agglomerative Hierarchical Clustering**

with:

- Number of clusters: **10**
- Linkage: **Ward**

The final model was selected based on comparative clustering evaluation and the interpretability of the resulting buyer profiles.

---

## 📏 Model Evaluation

The clustering models were evaluated using:

### Elbow Method

The Elbow Method was used to examine the change in within-cluster variation as the number of clusters increased.

### Silhouette Score

Silhouette Score was used to compare the relative quality of clustering structures.

The final Agglomerative model with 10 clusters achieved a silhouette score of approximately **0.195**.

The relatively low score indicates that the buyer groups have overlapping characteristics. Therefore, the resulting clusters are interpreted as exploratory buyer profiles rather than completely separated market categories.

---

## 👥 Final Buyer Segments

The final clustering model produced **10 buyer segments**.

| Cluster | Descriptive Segment |
|---|---|
| 0 | Agency Home Buyers |
| 1 | Website-Financed Home Buyers |
| 2 | Higher-Value Home Buyers |
| 3 | Mixed-Purpose Client-Referred Buyers |
| 4 | Agency Investment Buyers |
| 5 | Website Investment Buyers |
| 6 | Financed Investment Buyers |
| 7 | Older Active Home Buyers |
| 8 | Agency-Financed Home Buyers |
| 9 | High-Activity Property Buyers |

These names were assigned after examining the characteristics of each cluster. They are descriptive labels rather than predefined categories.

---

## 📈 Key Business Insights

The clustering analysis revealed several observable patterns:

- Some clusters were primarily associated with home acquisition, while others were investment-oriented.
- Financing behavior varied considerably between segments.
- Referral channels differed across buyer groups, including Website, Agency, and Client referrals.
- Some segments showed substantially higher property activity than others.
- One smaller segment demonstrated notably higher property activity and total property value exposure.
- Geographic variables were useful for profiling the identified segments but were excluded from the final clustering process to reduce geographic dominance.
- Buyer profiles can therefore be examined using a combination of behavioral, demographic, financing, and property-related characteristics.

These insights can support more targeted marketing and buyer analysis strategies.

---

## 📊 Interactive Streamlit Dashboard

An interactive Streamlit dashboard was developed to make the analysis easier to explore.

### Dashboard Features

- **Buyer Segmentation Overview**
  - Cluster distribution
  - Segment sizes
  - Buyer profile summary

- **Buyer Behavior Analysis**
  - Property activity
  - Property value
  - Acquisition purpose
  - Financing behavior
  - Referral channels

- **Geographic Buyer Analysis**
  - Country-level buyer distribution
  - Regional analysis
  - Geographic segment patterns

- **Segment Explorer**
  - Cluster-specific statistics
  - Descriptive buyer profiles
  - Segment-level comparisons

- **Interactive Filters**
  - Country
  - Region
  - Acquisition purpose
  - Client type

- **ML Methodology**
  - Feature preparation
  - Clustering approach
  - Model evaluation

---

## 🛠️ Technologies Used

### Programming
- Python

### Data Analysis
- Pandas
- NumPy

### Machine Learning
- Scikit-learn

### Visualization
- Plotly
- Matplotlib
- Seaborn

### Dashboard
- Streamlit

### Development Environment
- Jupyter Notebook
- VS Code

### Version Control
- Git
- GitHub

---

## 📁 Project Structure

```text
Real_estate_ml_project/
│
├── data/
│   └── dashboard_data.csv
│
├── notebook/
│   └── project notebooks
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md