import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="Churn Pattern Analytics in European Banking",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    # Customer Segmentation & Churn Pattern Analytics in European Banking

    **Analyzing customer segments, churn behavior, engagement patterns, and financial risk**
    ---
    """
)


st.markdown(
    """
    <style>

    .main {
        background-color: #020617;
    }

    .stApp {
        background: linear-gradient(to right, #020617, #0F172A);
        color: white;
    }

    h1,h2,h3,h4,h5 {
        color: white;
        font-family: 'Segoe UI';
    }

    .metric-card {
        background: linear-gradient(145deg,#111827,#1E293B);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #334155;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }

    section[data-testid="stSidebar"] {
        background: #0F172A;
    }

    .stDataFrame {
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

#css block

st.markdown("""
<style>
/* ── Sidebar Filter Accent Override ── */

/* Selectbox & Multiselect selected highlight */
section[data-testid="stSidebar"] [data-baseweb="select"] [aria-selected="true"],
section[data-testid="stSidebar"] [data-baseweb="option"]:hover,
section[data-testid="stSidebar"] [data-baseweb="option"][aria-selected="true"] {
    background: linear-gradient(90deg, #1E3A5F 0%, #1A4A6B 100%) !important;
    color: #E0F0FF !important;
}

/* Multiselect tags/pills */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: linear-gradient(90deg, #1B3A5C 0%, #1E5070 100%) !important;
    color: #BAD9F5 !important;
    border: none !important;
}

/* Radio button selected dot */
section[data-testid="stSidebar"] [data-testid="stRadio"] input:checked + div,
section[data-testid="stSidebar"] input[type="radio"]:checked + label {
    color: #60A5FA !important;
}
section[data-testid="stSidebar"] [role="radio"][aria-checked="true"] {
    background: linear-gradient(135deg, #1D4ED8 0%, #0891B2 100%) !important;
    border-color: #3B82F6 !important;
}

/* Slider thumb & active track */
section[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {
    background: linear-gradient(135deg, #2563EB 0%, #0891B2 100%) !important;
    border-color: #60A5FA !important;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderTrackFill"] {
    background: linear-gradient(90deg, #1D4ED8 0%, #0EA5E9 100%) !important;
}

/* Checkbox checked state */
section[data-testid="stSidebar"] input[type="checkbox"]:checked + div {
    background: linear-gradient(135deg, #1D4ED8 0%, #0891B2 100%) !important;
    border-color: #3B82F6 !important;
}

/* Active/focused input border */
section[data-testid="stSidebar"] [data-baseweb="select"] div:focus-within,
section[data-testid="stSidebar"] [data-baseweb="input"]:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
}

/* Dropdown menu background */
[data-baseweb="popover"] ul,
[data-baseweb="menu"] {
    background: #0F172A !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 8px !important;
}
[data-baseweb="menu"] li:hover {
    background: linear-gradient(90deg, #1E3A5F 0%, #1A4A6B 100%) !important;
}
</style>
""", unsafe_allow_html=True)
# LOAD DATA

@st.cache_data
def load_data():

    df = pd.read_csv("European_Bank.csv")

    # Remove duplicates
    df = df.drop_duplicates()

    # Column cleaning
    df.columns = (
        df.columns
        .str.replace(' ','_')
        .str.replace('-','_')
        .str.strip()
    )

    st.write(df.columns.tolist())


    # Feature Engineering

    # Age Group
    df['Age_Group'] = pd.cut(
        df['Age'],
        bins=[0,30,45,60,100],
        labels=['<30','30-45','46-60','60+']
    )


    # Balance Segment
    df['Balance_Segment'] = pd.cut(
        df['Balance'],
        bins=[-1,0,50000,100000,float('inf')],
        labels=[
            'Zero Balance',
            'Low Balance',
            'Medium Balance',
            'High Balance'
        ]
    )


    # Churn Status
    df['Churn_Status'] = df['Exited'].map({
        0:'Retained',
        1:'Churned'
    })


    # Engagement Status
    df['Engagement_Status'] = df['IsActiveMember'].map({
        0:'Inactive',
        1:'Active'
    })


    # High Value Customer
    df['High_Value_Customer'] = np.where(
        df['Balance'] > 100000,
        'High Value',
        'Regular'
    )


    # High Value Churned
    df['High_Value_Churned'] = np.where(
        (df['Balance'] > 100000) &
        (df['Exited'] == 1),
        'High Value Churned',
        'Other'
    )


    return df


# call function
df = load_data()


# SIDEBAR

st.sidebar.title("Filters")

geography = st.sidebar.multiselect(
    "Select Geography",
    options=df["Geography"].unique()
)


gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique()
)


age_group = st.sidebar.multiselect(
    "Select Age Group",
    options=df["Age_Group"].unique()
)

# Balance Segment filter
balance_segment = st.sidebar.multiselect(
    "Select Balance Segment",
    options=df["Balance_Segment"].unique()
)


# Churn Status filter
churn_status = st.sidebar.multiselect(
    "Select Churn Status",
    options=df["Churn_Status"].unique()
)


# Engagement Status filter
engagement_status = st.sidebar.multiselect(
    "Select Engagement Status",
    options=df["Engagement_Status"].unique()
)


# High Value Customer filter
high_value = st.sidebar.multiselect(
    "Select Customer Value",
    options=df["High_Value_Customer"].unique()
)


# High Value Churned filter
high_value_churn = st.sidebar.multiselect(
    "Select High Value Churn Status",
    options=df["High_Value_Churned"].unique()
)



filtered_df = df.copy()


if geography:
    filtered_df = filtered_df[
        filtered_df["Geography"].isin(geography)
    ]


if gender:
    filtered_df = filtered_df[
        filtered_df["Gender"].isin(gender)
    ]


if age_group:
    filtered_df = filtered_df[
        filtered_df["Age_Group"].isin(age_group)
    ]


if balance_segment:
    filtered_df = filtered_df[
        filtered_df["Balance_Segment"].isin(balance_segment)
    ]


if churn_status:
    filtered_df = filtered_df[
        filtered_df["Churn_Status"].isin(churn_status)
    ]


if engagement_status:
    filtered_df = filtered_df[
        filtered_df["Engagement_Status"].isin(engagement_status)
    ]


if high_value:
    filtered_df = filtered_df[
        filtered_df["High_Value_Customer"].isin(high_value)
    ]


if high_value_churn:
    filtered_df = filtered_df[
        filtered_df["High_Value_Churned"].isin(high_value_churn)
    ]    

age_churn = (
    filtered_df
    .groupby("Age_Group")["Exited"]
    .mean()
    .reset_index()
)

age_churn["Exited"] = age_churn["Exited"] * 100

# DEBUG CHECK
st.write("Total Rows:", len(df))
st.write("Filtered Rows:", len(filtered_df))

# ================= KPI CALCULATIONS =================


# 1. Overall Churn Rate
overall_churn_rate = (
    filtered_df["Exited"].sum() /
    len(filtered_df)
) * 100



# 2. Engagement Drop Indicator
# Churn rate among inactive customers

inactive_customers = filtered_df[
    filtered_df["IsActiveMember"] == 0
]

engagement_drop_indicator = (
    inactive_customers["Exited"].sum() /
    len(inactive_customers)
) * 100 if len(inactive_customers) > 0 else 0



# 3. High Value Churn Rate

high_value_customers = filtered_df[
    filtered_df["High_Value_Customer"] == "High Value"
]

high_value_churn_rate = (
    high_value_customers["Exited"].sum() /
    len(high_value_customers)
) * 100 if len(high_value_customers) > 0 else 0



# 4. Lost Balance / Revenue Risk

lost_balance = filtered_df[
    filtered_df["Exited"] == 1
]["Balance"].sum()

# Engagement Drop Indicator KPI

inactive_customers = filtered_df[
    filtered_df["IsActiveMember"] == 0
]

engagement_drop = (
    inactive_customers["Exited"].sum()
    /
    len(inactive_customers)
) * 100 if len(inactive_customers) > 0 else 0



# KPI CARDS---------------

def colored_metric(col, bg_color, text_color, icon, label, value, sub):
    col.markdown(f"""
        <div style="
            background:{bg_color};
            color:{text_color};
            border-radius:14px;
            padding:1.1rem 1.25rem;
            display:flex;
            flex-direction:column;
            gap:6px;
        ">
            <div style="font-size:22px;">{icon}</div>
            <div style="font-size:12px;font-weight:500;opacity:0.85;">{label}</div>
            <div style="font-size:26px;font-weight:500;line-height:1.1;">{value}</div>
            <div style="font-size:11px;opacity:0.75;">{sub}</div>
        </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

colored_metric(col1, "#185FA5", "#E6F1FB", "👥",
               "Overall churn rate", f"{overall_churn_rate:.2f}%", "All customers")

colored_metric(col2, "#0F6E56", "#E1F5EE", "📉",
               "Engagement drop", f"{engagement_drop:.2f}%", "vs. previous period")

colored_metric(col3, "#993C1D", "#FAECE7", "👑",
               "High-value churn", f"{high_value_churn_rate:.2f}%", "Top-tier customers")

colored_metric(col4, "#534AB7", "#EEEDFE", "💸",
               "Lost balance", f"{lost_balance/1_000_000:.2f}M", "Total revenue lost")


# CHART 1: OVERALL CHURN RATE BY AGE GROUP

# Clustered Bar Chart

# Rename Exited column to Churn_Rate
age_churn["Churn_Rate"] = age_churn["Exited"] * 100


fig = px.bar(
    age_churn,
    x="Age_Group",
    y="Churn_Rate",
    title="CHURN RATE BY AGE GROUP",
    text="Churn_Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%"
)

st.plotly_chart(fig, use_container_width=True)

# CHART 6 (UPDATED): FINANCIAL PROFILE - AVG SALARY VS AVG BALANCE BY BALANCE SEGMENT & CHURN STATUS

financial_profile = (
    filtered_df
    .groupby(["Balance_Segment", "Churn_Status"])
    .agg(
        Avg_Balance=("Balance", "mean"),
        Avg_Salary=("EstimatedSalary", "mean"),
        Customer_Count=("Exited", "count")
    )
    .reset_index()
)

fig6 = px.scatter(
    financial_profile,
    x="Avg_Salary",
    y="Avg_Balance",
    color="Churn_Status",
    size="Customer_Count",
    text="Balance_Segment",
    title="Financial Profile: SALARY vs BALANCE BY CHURN STATUS",
    color_discrete_map={
        "Retained": "#0EA5E9",
        "Churned": "#F97316"
    }
)

fig6.update_traces(
    marker=dict(line=dict(width=1, color="#0F172A")),
    textposition="top center",
    textfont=dict(color="white", size=10)
)

fig6.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    legend=dict(font=dict(color="white")),
    xaxis_title="Average Estimated Salary",
    yaxis_title="Average Balance"
)

st.plotly_chart(fig6, use_container_width=True)

# CHART 2: OVERALL CHURN RATE BY BALANCE SEGMENT

balance_churn = (
    filtered_df
    .groupby("Balance_Segment")["Exited"]
    .mean()
    .reset_index()
)

balance_churn["Churn_Rate"] = balance_churn["Exited"] * 100

fig2 = px.bar(
    balance_churn,
    x="Churn_Rate",
    y="Balance_Segment",
    title="CHURN BY BALANCE SEGMENT",
    text="Churn_Rate",
    color="Balance_Segment"
)

fig2.update_traces(
    texttemplate="%{text:.2f}%"
)

st.plotly_chart(fig2, use_container_width=True)

# CHART 3: OVERALL CHURN RATE BY ENGAGEMENT STATUS

engagement_churn = (
    filtered_df
    .groupby("Engagement_Status")["Exited"]
    .mean()
    .reset_index()
)

engagement_churn["Churn_Rate"] = engagement_churn["Exited"] * 100

fig3 = px.bar(
    engagement_churn,
    x="Engagement_Status",
    y="Churn_Rate",
    title=" CHURN RATE BY CUSTOMER ENGAGEMENT STATUS",
    text="Churn_Rate",
    color="Engagement_Status"
)

fig3.update_traces(
    texttemplate="%{text:.2f}%"
)

st.plotly_chart(fig3, use_container_width=True)


# CHART 4: HIGH VALUE CUSTOMER CHURN DISTRIBUTION (DONUT)

high_value_df = filtered_df[
    filtered_df["High_Value_Customer"] == "High Value"
]

hv_churn_dist = (
    high_value_df["Churn_Status"]
    .value_counts()
    .reset_index()
)
hv_churn_dist.columns = ["Churn_Status", "Count"]

fig4 = px.pie(
    hv_churn_dist,
    names="Churn_Status",
    values="Count",
    title="HIGH VALUE CUSTOMER CHURN DISTRIBUTION",
    hole=0.55,
    color="Churn_Status",
    color_discrete_map={
        "Retained": "#0EA5E9",
        "Churned": "#F97316"
    }
)

fig4.update_traces(
    textinfo="label+percent",
    textfont_size=13,
    marker=dict(line=dict(color="#0F172A", width=2))
)

fig4.update_layout(
    showlegend=True,
    legend=dict(font=dict(color="white")),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)

st.plotly_chart(fig4, use_container_width=True)

# CHART 5: OVERALL CHURN RATE BY GEOGRAPHY & GENDER (CLUSTERED)

geo_gender_churn = (
    filtered_df
    .groupby(["Geography", "Gender"])["Exited"]
    .mean()
    .reset_index()
)

geo_gender_churn["Churn_Rate"] = geo_gender_churn["Exited"] * 100

fig5 = px.bar(
    geo_gender_churn,
    x="Geography",
    y="Churn_Rate",
    color="Gender",
    barmode="group",
    title="CHURN RATE BY GEOGRAPHY AND GENDER",
    text="Churn_Rate",
    color_discrete_map={
        "Male": "#3B82F6",
        "Female": "#F472B6"
    }
)

fig5.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig5.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    legend=dict(font=dict(color="white")),
    yaxis_title="Churn Rate (%)"
)

st.plotly_chart(fig5, use_container_width=True)


# CHART 7: AGE & TENURE CHURN COMPARISON (HEATMAP)

age_tenure_churn = (
    filtered_df
    .groupby(["Age_Group", "Tenure"])["Exited"]
    .mean()
    .reset_index()
)

age_tenure_churn["Churn_Rate"] = age_tenure_churn["Exited"] * 100

age_tenure_pivot = age_tenure_churn.pivot(
    index="Age_Group",
    columns="Tenure",
    values="Churn_Rate"
)

fig7 = px.imshow(
    age_tenure_pivot,
    text_auto=".1f",
    aspect="auto",
    color_continuous_scale=[
        [0, "#0F172A"],
        [0.5, "#1D4ED8"],
        [1, "#F97316"]
    ],
    title="Age & Tenure Churn Rate Comparison (%)"
)

fig7.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    coloraxis_colorbar=dict(title="Churn %", tickfont=dict(color="white")),
    xaxis_title="Tenure (Years)",
    yaxis_title="Age Group"
)

st.plotly_chart(fig7, use_container_width=True)