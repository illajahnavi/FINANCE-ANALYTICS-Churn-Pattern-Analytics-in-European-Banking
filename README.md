# FINANCE-ANALYTICS-Churn-Pattern-Analytics-in-European-Banking
# Customer Segmentation & Churn Pattern Analytics in European Banking 📊

PROJECT OVERVIEW 

Customer churn is one of the major challenges in the banking industry. Losing existing customers impacts customer lifetime value, increases acquisition costs, and creates revenue instability.

This project focuses on analyzing customer churn patterns in European banking using customer segmentation, financial analysis, engagement analysis, and demographic insights.

The dashboard helps identify:
- High-risk customer segments
- Geographic and demographic churn patterns
- Financial impact of customer exits
- High-value customer churn risk
- Engagement factors influencing churn

The project was developed using **Python, Streamlit, Pandas, NumPy, and Plotly** to create an interactive analytics dashboard.

---

BUSINESS PROBLEM

Banks have large volumes of customer data but often struggle to answer:

- Which customers are most likely to churn?
- Which regions have higher churn risk?
- Are high-value customers leaving?
- How does customer engagement affect churn?
- What financial impact does churn create?

PROJECT OBJECTIVES

## Primary Objectives

- Calculate overall customer churn rate
- Analyze churn distribution across customer segments
- Compare churn behavior across European regions

## Secondary Objectives

- Identify high-value customer churn risk
- Analyze customer engagement patterns
- Evaluate age and tenure impact on churn
- Quantify financial impact of customer exits
- Support data-driven retention strategies

---

DATASET DESCRIPTION

The dataset contains customer-level banking information.

| Column | Description |
|---|---|
| CustomerId | Unique customer identifier |
| CreditScore | Customer creditworthiness |
| Geography | Customer location (France, Spain, Germany) |
| Gender | Customer gender |
| Age | Customer age |
| Tenure | Years with bank |
| Balance | Account balance |
| NumOfProducts | Number of banking products |
| HasCrCard | Credit card ownership |
| IsActiveMember | Customer engagement indicator |
| EstimatedSalary | Estimated annual salary |
| Exited | Customer churn indicator |

---

DATA PREPARATION AND FEATURE ENGINEERING

The project includes multiple derived features:
Age Group Segmentation
Customers are grouped into:
- <30
- 30–45
- 46–60
- 60+

Balance Segmentation
Customers are categorized as:
- Zero Balance
- Low Balance
- Medium Balance
- High Balance

High Value Customer Identification
Customers with higher account balances are classified as:
- High Value
- Regular

High Value Churn Analysis
Identifies customers who are:
- High balance customers
- AND churned customers

REQUIREMENTS

-streamlit
-pandas
-numpy
-plotly

Business Recommendations

Based on analysis:
-Develop targeted retention strategies for high-risk customers
-Improve engagement among inactive customers
-Focus on high-value customer retention
-Create region-specific strategies for high churn areas
-Monitor customer behavior before churn occurs
