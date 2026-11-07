# Customer Churn & Retention Analytics

An end-to-end customer churn and retention analytics project using **Python, MySQL, Excel, Streamlit, and Tableau** to identify customer churn patterns, understand retention trends, and generate actionable business insights.

## 📌 Project Overview

Customer churn is a major challenge for subscription-based businesses. Understanding why customers leave helps businesses improve customer satisfaction, strengthen retention strategies, and reduce revenue risks.

This project analyzes the IBM Telco Customer Churn dataset to explore customer behavior, identify factors associated with churn, and visualize important business metrics through interactive dashboards.

## 🎯 Project Objectives

- Analyze overall customer churn and retention rates.
- Identify customer segments with higher churn rates.
- Evaluate the relationship between contract types and churn.
- Analyze churn patterns across internet services and payment methods.
- Understand the impact of customer tenure on churn.
- Examine monthly charges and revenue associated with churned customers.
- Build interactive dashboards to communicate business insights.

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Python | Data cleaning, preprocessing and exploratory data analysis |
| Pandas & NumPy | Data manipulation and analysis |
| Matplotlib & Seaborn | Exploratory data visualizations |
| MySQL | Data querying and business analysis |
| Excel | PivotTables, charts and exploratory analysis |
| Streamlit | Interactive analytical dashboard |
| Tableau Public | Interactive visualizations and dashboard |
| GitHub | Project version control and documentation |

## 📂 Project Structure

```text
Customer-Churn-Retention-Analytics/
│
├── data/
│   
│   └── cleaned_customer_churn.csv
│
├── python/
│   ├── 01_data_inspection.py
│   ├── 02_data_cleaning.py
│   ├── 03_service_churn_analysis.py
│   └── 04_churn_revenue_analysis.py
│
├── sql/
│   ├── analysis.sql
│   └── customer_churn_analysis.sql
│
├── excel/
│   ├── Customer_Churn_Analysis.xlsx
│   └── excel_analysis_findings.txt
│
├── screenshots/
│
├── streamlit_dashboard/
│   └── app.py
│
├── tableau/
│
├── requirements.txt
├── .gitignore
└── README.md
```


## 📊 Dataset Information

**Dataset:** IBM Telco Customer Churn

**Source:** [IBM Telco Customer Churn Dataset](https://github.com/IBM/telco-customer-churn-on-icp4d)

- Total records: 7,043 customers
- Total columns: 21
- Target variable: Churn
- Data includes customer demographics, subscription services, contract details, payment methods, tenure and charges.

## 🧹 Data Cleaning & Preparation

Data cleaning and preprocessing were performed using Python.

Key activities:
- Inspected dataset structure and data types.
- Checked missing values and duplicate records.
- Converted `TotalCharges` into a numeric data type.
- Handled blank `TotalCharges` values for customers with zero tenure.
- Verified the cleaned dataset.
- Exported the processed data into a separate CSV file.

## 🔍 Exploratory Data Analysis

The analysis explored:

- Customer demographics and senior citizen status.
- Contract type and internet service.
- Additional subscription services.
- Payment methods.
- Customer tenure groups.
- Monthly charges and total charges.
- Churn and retention patterns.

## 🗄️ SQL Analysis

MySQL was used to perform business-oriented queries, including:

- Overall churn and retention rate.
- Churn rate by contract type.
- Churn rate by internet service.
- Churn by tenure groups.
- Churn by payment method.
- Churn by senior citizen status.
- Churn across additional subscription services.
- Monthly charges and revenue analysis.

## 📈 Key Business Findings

The analysis revealed the following patterns:

| Business Metric | Result |
|---|---:|
| Total Customers | 7,043 |
| Churned Customers | 1,869 |
| Retained Customers | 5,174 |
| Overall Churn Rate | 26.54% |
| Retention Rate | 73.46% |

### Important Insights

**1. Contract Type**
- Month-to-month customers have the highest churn rate at 42.71%.
- One-year contract customers have an 11.27% churn rate.
- Two-year contract customers have the lowest churn rate at 2.83%.

**2. Internet Service**
- Fiber optic customers have a churn rate of 41.89%.
- DSL customers have a churn rate of 18.96%.
- Customers without internet service have a churn rate of 7.40%.

**3. Customer Tenure**
- Customers with shorter tenure show higher churn rates.
- The first 12 months represent an important customer retention period.

**4. Payment Method**
- Customers using electronic checks show a higher churn rate than customers using other payment methods.

**5. Additional Services**
- Customers without services such as Online Security and Tech Support show higher churn rates.

## 💡 Business Recommendations

Based on the analysis:

- Introduce loyalty programs and incentives to encourage longer-term contracts.
- Focus on onboarding and engagement during the first 12 months.
- Investigate service-related dissatisfaction among fiber optic customers.
- Encourage automatic payment options where appropriate.
- Offer targeted support and additional services to high-risk customer segments.
- Monitor customer churn regularly using interactive dashboards.

## 📊 Interactive Dashboards

The project includes dashboard development using Streamlit and Tableau Public.

Dashboard components include:
- Customer and churn KPIs.
- Churn distribution.
- Churn by contract type.
- Churn by internet service.
- Churn by tenure.
- Churn by payment method.
- Customer risk analysis.

Screenshots of the dashboards and visualizations are available in the `screenshots/` folder.

## 🚀 Running the Streamlit Dashboard

1. Clone the repository:

```bash
git clone https://github.com/fiyonaann/customer-churn-retention-analytics.git
```

2. Navigate to the project directory:

```bash
cd customer-churn-retention-analytics
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the dashboard:

```bash
streamlit run streamlit_dashboard/app.py
```

## 📚 Skills Demonstrated

- Data Cleaning and Preprocessing
- Exploratory Data Analysis (EDA)
- SQL Querying and Aggregation
- Customer Segmentation
- Churn and Retention Analysis
- Data Visualization
- Dashboard Development
- Business Insight Generation

## 👩‍💻 Author

**Fiyona Ann Sojan**

Computer Science and Engineering

GitHub: [@fiyonaann](https://github.com/fiyonaann)

---

*This project was developed as part of my data analytics portfolio to demonstrate practical skills in data analysis, SQL, visualization, and business intelligence.*
