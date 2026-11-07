from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Customer Churn & Retention Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATA LOADING
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

REQUIRED_COLUMNS = [
    "customerID",
    "tenure",
    "Contract",
    "InternetService",
    "MonthlyCharges",
    "TotalCharges",
    "Churn"
]


@st.cache_data
def load_data():
    """
    Load the original or cleaned Telco customer dataset.
    Reject Excel PivotTable exports and other incorrect CSVs.
    """

    possible_files = [
        DATA_DIR / "cleaned_customer_churn.csv",
        DATA_DIR / "Telco-Customer-Churn.csv",
    ]

    errors = []

    for file_path in possible_files:
        if not file_path.exists():
            continue

        try:
            data = pd.read_csv(file_path)
            data.columns = data.columns.astype(str).str.strip()

            missing = [
                column for column in REQUIRED_COLUMNS
                if column not in data.columns
            ]

            if missing:
                errors.append(
                    f"{file_path.name}: missing {', '.join(missing)}"
                )
                continue

            # Prefer a valid cleaned dataset. If the cleaned file
            # is actually a PivotTable export, try the original.
            data["tenure"] = pd.to_numeric(
                data["tenure"], errors="coerce"
            )

            data["MonthlyCharges"] = pd.to_numeric(
                data["MonthlyCharges"], errors="coerce"
            )

            data["TotalCharges"] = pd.to_numeric(
                data["TotalCharges"], errors="coerce"
            )

            data["Churn"] = (
                data["Churn"].astype(str).str.strip()
            )

            data = data[
                data["Churn"].isin(["Yes", "No"])
            ].copy()

            if data.empty:
                errors.append(
                    f"{file_path.name}: no valid Yes/No churn records"
                )
                continue

            data["tenure"] = data["tenure"].fillna(0)
            data["MonthlyCharges"] = (
                data["MonthlyCharges"].fillna(0)
            )
            data["TotalCharges"] = (
                data["TotalCharges"].fillna(0)
            )

            # Additional fields used by the dashboard.
            data["ChurnStatus"] = data["Churn"].map({
                "Yes": "Churned",
                "No": "Retained"
            })

            data["TenureGroup"] = pd.cut(
                data["tenure"],
                bins=[-1, 12, 24, 48, 72],
                labels=[
                    "0–12 months",
                    "13–24 months",
                    "25–48 months",
                    "49–72 months"
                ],
                include_lowest=True
            )

            return data, file_path.name

        except Exception as error:
            errors.append(
                f"{file_path.name}: {error}"
            )

    error_details = "\n".join(errors) if errors else (
        "Neither expected CSV file was found."
    )

    raise FileNotFoundError(
        "Could not load a valid Telco customer dataset.\n\n"
        f"Expected folder: {DATA_DIR}\n\n"
        f"Details:\n{error_details}"
    )


# =========================================================
# LOAD AND VALIDATE DATA
# =========================================================

try:
    df, source_file = load_data()

except Exception as error:
    st.error("Unable to load the customer churn dataset.")
    st.code(str(error))

    st.info(
        "Check that your data folder contains "
        "'Telco-Customer-Churn.csv' or a valid "
        "'cleaned_customer_churn.csv'. "
        "The file must contain the original customer records, "
        "not an Excel PivotTable export."
    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📊 Churn Analytics")

st.sidebar.caption("Customer Retention Dashboard")

st.sidebar.success(
    f"Dataset loaded: {source_file}"
)

st.sidebar.markdown("---")

st.sidebar.subheader("Filter Customers")

contract_options = sorted(
    df["Contract"].dropna().astype(str).unique().tolist()
)

selected_contracts = st.sidebar.multiselect(
    "Contract Type",
    options=contract_options,
    default=contract_options
)

internet_options = sorted(
    df["InternetService"].dropna().astype(str).unique().tolist()
)

selected_internet = st.sidebar.multiselect(
    "Internet Service",
    options=internet_options,
    default=internet_options
)

min_tenure = int(df["tenure"].min())
max_tenure = int(df["tenure"].max())

selected_tenure = st.sidebar.slider(
    "Customer Tenure (Months)",
    min_value=min_tenure,
    max_value=max_tenure,
    value=(min_tenure, max_tenure)
)

churn_options = ["Yes", "No"]

selected_churn = st.sidebar.multiselect(
    "Churn Status",
    options=churn_options,
    default=churn_options,
    format_func=lambda value: (
        "Churned" if value == "Yes" else "Retained"
    )
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    df["Contract"].astype(str).isin(selected_contracts)
    & df["InternetService"].astype(str).isin(selected_internet)
    & df["tenure"].between(
        selected_tenure[0],
        selected_tenure[1]
    )
    & df["Churn"].isin(selected_churn)
].copy()


# =========================================================
# HEADER
# =========================================================

st.title("📊 Customer Churn & Retention Analytics")

st.markdown(
    "Analyze customer churn, retention, contract types, "
    "internet services, tenure, and revenue."
)

st.caption(
    "Use the sidebar filters to explore different customer segments."
)

st.markdown("---")


# =========================================================
# KPI CARDS
# =========================================================

total_customers = len(filtered_df)

churned_customers = int(
    (filtered_df["Churn"] == "Yes").sum()
)

retained_customers = int(
    (filtered_df["Churn"] == "No").sum()
)

churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0 else 0
)

retention_rate = (
    retained_customers / total_customers * 100
    if total_customers > 0 else 0
)

total_monthly_charges = filtered_df[
    "MonthlyCharges"
].sum()

avg_monthly_charges = (
    filtered_df["MonthlyCharges"].mean()
    if total_customers > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Churned Customers",
    f"{churned_customers:,}"
)

col3.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

col4.metric(
    "Retention Rate",
    f"{retention_rate:.2f}%"
)

st.markdown("")

col5, col6 = st.columns(2)

col5.metric(
    "Total Monthly Charges",
    f"${total_monthly_charges:,.2f}"
)

col6.metric(
    "Average Monthly Charge",
    f"${avg_monthly_charges:,.2f}"
)

st.markdown("---")


# =========================================================
# CHART 1: CHURN DISTRIBUTION
# =========================================================

st.subheader("1. Customer Churn Overview")

if not filtered_df.empty:

    churn_summary = (
        filtered_df["ChurnStatus"]
        .value_counts()
        .rename_axis("Customer Status")
        .reset_index(name="Customers")
    )

    fig_churn = px.pie(
        churn_summary,
        names="Customer Status",
        values="Customers",
        title="Customer Churn vs Retention",
        hole=0.45,
        color="Customer Status",
        color_discrete_map={
            "Churned": "#EF553B",
            "Retained": "#00CC96"
        }
    )

    fig_churn.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_churn,
        use_container_width=True
    )

else:
    st.info("No customers match the selected filters.")


# =========================================================
# CHART 2: CHURN BY CONTRACT
# =========================================================

st.subheader("2. Churn by Contract Type")

if not filtered_df.empty:

    contract_summary = (
        filtered_df.groupby(
            "Contract",
            observed=True
        )
        .agg(
            Total_Customers=("customerID", "count"),
            Churned_Customers=(
                "Churn",
                lambda values: (values == "Yes").sum()
            )
        )
        .reset_index()
    )

    contract_summary["Churn Rate (%)"] = (
        contract_summary["Churned_Customers"]
        / contract_summary["Total_Customers"]
        * 100
    )

    fig_contract = px.bar(
        contract_summary,
        x="Contract",
        y="Churn Rate (%)",
        text="Churn Rate (%)",
        title="Churn Rate by Contract Type",
        color="Churn Rate (%)",
        color_continuous_scale="Reds"
    )

    fig_contract.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_contract.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Contract Type",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_contract,
        use_container_width=True
    )


# =========================================================
# CHART 3: CHURN BY INTERNET SERVICE
# =========================================================

st.subheader("3. Churn by Internet Service")

if not filtered_df.empty:

    internet_summary = (
        filtered_df.groupby(
            "InternetService",
            observed=True
        )
        .agg(
            Total_Customers=("customerID", "count"),
            Churned_Customers=(
                "Churn",
                lambda values: (values == "Yes").sum()
            )
        )
        .reset_index()
    )

    internet_summary["Churn Rate (%)"] = (
        internet_summary["Churned_Customers"]
        / internet_summary["Total_Customers"]
        * 100
    )

    fig_internet = px.bar(
        internet_summary,
        x="InternetService",
        y="Churn Rate (%)",
        color="InternetService",
        text="Churn Rate (%)",
        title="Churn Rate by Internet Service"
    )

    fig_internet.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_internet.update_layout(
        xaxis_title="Internet Service",
        yaxis_title="Churn Rate (%)",
        showlegend=False
    )

    st.plotly_chart(
        fig_internet,
        use_container_width=True
    )


# =========================================================
# CHART 4: TENURE ANALYSIS
# =========================================================

st.subheader("4. Customer Churn by Tenure")

if not filtered_df.empty:

    tenure_summary = (
        filtered_df.groupby(
            "TenureGroup",
            observed=False
        )
        .agg(
            Total_Customers=("customerID", "count"),
            Churned_Customers=(
                "Churn",
                lambda values: (values == "Yes").sum()
            )
        )
        .reset_index()
    )

    tenure_summary = tenure_summary[
        tenure_summary["Total_Customers"] > 0
    ].copy()

    tenure_summary["Churn Rate (%)"] = (
        tenure_summary["Churned_Customers"]
        / tenure_summary["Total_Customers"]
        * 100
    )

    fig_tenure = px.bar(
        tenure_summary,
        x="TenureGroup",
        y="Churn Rate (%)",
        text="Churn Rate (%)",
        title="Churn Rate Across Customer Tenure Groups",
        color="Churn Rate (%)",
        color_continuous_scale="Oranges"
    )

    fig_tenure.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_tenure.update_layout(
        xaxis_title="Tenure Group",
        yaxis_title="Churn Rate (%)",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_tenure,
        use_container_width=True
    )


# =========================================================
# CHART 5: MONTHLY CHARGES
# =========================================================

st.subheader("5. Monthly Charges by Churn Status")

if not filtered_df.empty:

    fig_charges = px.box(
        filtered_df,
        x="ChurnStatus",
        y="MonthlyCharges",
        color="ChurnStatus",
        color_discrete_map={
            "Churned": "#EF553B",
            "Retained": "#00CC96"
        },
        title="Monthly Charges Distribution"
    )

    fig_charges.update_layout(
        xaxis_title="Customer Status",
        yaxis_title="Monthly Charges ($)",
        showlegend=False
    )

    st.plotly_chart(
        fig_charges,
        use_container_width=True
    )


# =========================================================
# CUSTOMER DATA TABLE
# =========================================================

st.markdown("---")

st.subheader("6. Customer Data Explorer")

search_text = st.text_input(
    "Search by Customer ID",
    placeholder="Enter a customer ID..."
)

display_df = filtered_df.copy()

if search_text.strip():
    display_df = display_df[
        display_df["customerID"]
        .astype(str)
        .str.contains(
            search_text.strip(),
            case=False,
            na=False
        )
    ]

display_columns = [
    column for column in [
        "customerID",
        "gender",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "tenure",
        "Contract",
        "InternetService",
        "MonthlyCharges",
        "TotalCharges",
        "Churn"
    ]
    if column in display_df.columns
]

st.dataframe(
    display_df[display_columns],
    use_container_width=True,
    hide_index=True
)

csv_data = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Customer Data",
    data=csv_data,
    file_name="filtered_customer_churn.csv",
    mime="text/csv"
)


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.markdown("---")

st.subheader("7. Business Insights")

if not filtered_df.empty:

    insights = []

    if churn_rate > 0:
        insights.append(
            f"**Churn:** {churn_rate:.2f}% of the currently "
            "filtered customers have churned."
        )

    if not contract_summary.empty:
        highest_contract = contract_summary.loc[
            contract_summary["Churn Rate (%)"].idxmax()
        ]

        insights.append(
            f"**Contract risk:** "
            f"{highest_contract['Contract']} contracts have the "
            f"highest observed churn rate "
            f"({highest_contract['Churn Rate (%)']:.2f}%)."
        )

    if not internet_summary.empty:
        highest_internet = internet_summary.loc[
            internet_summary["Churn Rate (%)"].idxmax()
        ]

        insights.append(
            f"**Internet service:** "
            f"{highest_internet['InternetService']} has the "
            f"highest observed churn rate "
            f"({highest_internet['Churn Rate (%)']:.2f}%)."
        )

    for insight in insights:
        st.markdown(f"- {insight}")

    st.caption(
        "These are descriptive associations, not proof of causation. "
        "Monthly charges associated with churned customers should not "
        "be interpreted as guaranteed recoverable revenue."
    )

else:
    st.info(
        "Select filters that include customers to display business insights."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Customer Churn & Retention Analytics | "
    "Python • Pandas • Streamlit • Plotly"
)
