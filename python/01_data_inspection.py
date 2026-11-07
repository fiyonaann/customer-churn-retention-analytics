import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("data/Telco-Customer-Churn.csv")

# Display the first 5 rows
print("FIRST 5 ROWS:")
print(df.head())

# Display dataset dimensions
print("\nDATASET SHAPE:")
print(df.shape)

# Display column names
print("\nCOLUMN NAMES:")
print(df.columns.tolist())

# Display dataset information
print("\nDATASET INFORMATION:")
df.info()

# Check missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# Check duplicate records
print("\nDUPLICATE RECORDS:")
print(df.duplicated().sum())

# Display statistical summary
print("\nSTATISTICAL SUMMARY:")
print(df.describe(include="all"))


# Investigate TotalCharges
print("\nTOTALCHARGES DATA TYPE:")
print(df["TotalCharges"].dtype)

print("\nBLANK TOTALCHARGES:")
print((df["TotalCharges"].str.strip() == "").sum())

print("\nSAMPLE TOTALCHARGES VALUES:")
print(df["TotalCharges"].sample(10, random_state=42).tolist())

print("\nTENURE ZERO CUSTOMERS:")
print(df[df["tenure"] == 0][["customerID", "tenure", "TotalCharges"]])


# Analyze customer churn distribution
print("\nCUSTOMER CHURN DISTRIBUTION:")
print(df["Churn"].value_counts())

print("\nCUSTOMER CHURN PERCENTAGE:")
print(df["Churn"].value_counts(normalize=True).mul(100).round(2))

print("\nTOTAL CUSTOMERS:")
print(df["customerID"].nunique())


# Analyze churn by contract type
print("\nCHURN BY CONTRACT TYPE:")

contract_churn = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print(contract_churn.round(2))


# Analyze churn by customer tenure
df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 60, 72],
    labels=[
        "0-12 months",
        "13-24 months",
        "25-48 months",
        "49-60 months",
        "61-72 months"
    ]
)

print("\nCHURN BY TENURE GROUP:")

tenure_churn = pd.crosstab(
    df["TenureGroup"],
    df["Churn"],
    normalize="index"
) * 100

print(tenure_churn.round(2))

# VISUALIZATIONS..........................................................................
#  Visualize churn by contract type

plt.figure(figsize=(9, 5))

sns.countplot(
    data=df,
    x="Contract",
    hue="Churn",
    order=["Month-to-month", "One year", "Two year"]
)

plt.title("Customer Churn by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Number of Customers")
plt.legend(title="Churn")
plt.tight_layout()

plt.savefig(
    "python/churn_by_contract.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Visualize churn percentage by tenure group

tenure_churn_rate = (
    df.groupby("TenureGroup", observed=False)["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .reset_index(name="ChurnRate")
)

plt.figure(figsize=(10, 5))

sns.barplot(
    data=tenure_churn_rate,
    x="TenureGroup",
    y="ChurnRate"
)

plt.title("Customer Churn Rate by Tenure Group")
plt.xlabel("Customer Tenure")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=15)
plt.tight_layout()

plt.savefig(
    "python/churn_by_tenure.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Chart 3: Customer Churn Distribution

plt.figure(figsize=(8, 6))

sns.countplot(
    data=df,
    x="Churn"
)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn Status")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    "python/churn_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Chart 4: Customer Churn by Internet Service

plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="InternetService",
    hue="Churn"
)

plt.title("Customer Churn by Internet Service")
plt.xlabel("Internet Service Type")
plt.ylabel("Number of Customers")
plt.legend(title="Churn")
plt.tight_layout()

plt.savefig(
    "python/churn_by_internet_service.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 5: Customer Churn by Payment Method


payment_churn = pd.crosstab(
    df["PaymentMethod"],
    df["Churn"]
)

payment_churn = payment_churn.sort_values(
    by="Yes",
    ascending=True
)

payment_churn.plot(
    kind="barh",
    figsize=(10, 6),
    color=["#2A9D8F", "#E76F51"]
)

plt.title("Customer Churn by Payment Method", fontsize=14)
plt.xlabel("Number of Customers")
plt.ylabel("Payment Method")
plt.legend(title="Churn")
plt.tight_layout()

plt.savefig(
    "python/churn_by_payment_method.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 6: Monthly Charges vs Customer Churn

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="Churn",
    y="MonthlyCharges",
    hue="Churn",
    palette={"No": "#2A9D8F", "Yes": "#E76F51"},
    legend=False
)

plt.title("Monthly Charges by Customer Churn", fontsize=14)
plt.xlabel("Customer Churn")
plt.ylabel("Monthly Charges")
plt.tight_layout()

plt.savefig(
    "python/monthly_charges_by_churn.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 7: Customer Tenure Distribution

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df,
    x="tenure",
    bins=30,
    kde=True,
    color="#457B9D",
    edgecolor="white"
)

plt.title("Distribution of Customer Tenure", fontsize=14)
plt.xlabel("Tenure (Months)")
plt.ylabel("Number of Customers")
plt.tight_layout()

plt.savefig(
    "python/customer_tenure_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 8: Churn Rate by Contract Type - Heatmap

contract_churn_rate = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

plt.figure(figsize=(8, 5))

sns.heatmap(
    contract_churn_rate[["Yes"]],
    annot=True,
    fmt=".2f",
    cmap="YlOrRd",
    linewidths=1,
    cbar_kws={"label": "Churn Rate (%)"}
)

plt.title("Customer Churn Rate by Contract Type", fontsize=14)
plt.xlabel("Churn Status")
plt.ylabel("Contract Type")
plt.tight_layout()

plt.savefig(
    "python/churn_rate_contract_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 9: Churn Rate by Payment Method - 100% Stacked Bar Chart

payment_churn = pd.crosstab(
    df["PaymentMethod"],
    df["Churn"],
    normalize="index"
) * 100

payment_churn = payment_churn[["No", "Yes"]]

payment_churn.plot(
    kind="bar",
    stacked=True,
    figsize=(10, 6),
    color=["#2A9D8F", "#E76F51"],
    edgecolor="white",
    width=0.7
)

plt.title("Customer Churn by Payment Method", fontsize=14)
plt.xlabel("Payment Method")
plt.ylabel("Percentage of Customers (%)")
plt.xticks(rotation=25, ha="right")
plt.legend(title="Churn Status")
plt.ylim(0, 100)
plt.tight_layout()

plt.savefig(
    "python/churn_by_payment_method.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 10: Monthly Charges vs Customer Tenure

plt.figure(figsize=(10, 6))

sns.regplot(
    data=df,
    x="tenure",
    y="MonthlyCharges",
    scatter_kws={"alpha": 0.25, "s": 20},
    line_kws={"color": "red", "linewidth": 2},
    ci=None
)

plt.title("Relationship Between Customer Tenure and Monthly Charges")
plt.xlabel("Customer Tenure (Months)")
plt.ylabel("Monthly Charges")
plt.tight_layout()

plt.savefig(
    "python/monthly_charges_vs_tenure.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 11: Customer Churn Rate by Gender - Lollipop Chart

gender_churn = (
    df.groupby("gender")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .sort_values()
)

plt.figure(figsize=(8, 5))

plt.hlines(
    y=gender_churn.index,
    xmin=0,
    xmax=gender_churn.values,
    color="teal",
    linewidth=3
)

plt.scatter(
    gender_churn.values,
    gender_churn.index,
    color="coral",
    s=180,
    zorder=3
)

for gender, rate in gender_churn.items():
    plt.text(
        rate + 0.5,
        gender,
        f"{rate:.2f}%",
        va="center"
    )

plt.title("Customer Churn Rate by Gender")
plt.xlabel("Churn Rate (%)")
plt.ylabel("Gender")
plt.xlim(0, gender_churn.max() + 7)
plt.tight_layout()

plt.savefig(
    "python/churn_by_gender.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 12: Churn Rate by Senior Citizen Status

senior_churn = (
    df.groupby("SeniorCitizen")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

senior_churn.index = senior_churn.index.map({
    0: "Non-Senior Citizens",
    1: "Senior Citizens"
})

senior_churn = senior_churn.sort_values()

plt.figure(figsize=(9, 5))

bars = plt.barh(
    senior_churn.index,
    senior_churn.values,
    color=["#2A9D8F", "#E76F51"],
    height=0.55
)

for bar in bars:
    width = bar.get_width()
    plt.text(
        width + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.2f}%",
        va="center"
    )

plt.title("Customer Churn Rate by Senior Citizen Status")
plt.xlabel("Churn Rate (%)")
plt.ylabel("Customer Group")
plt.xlim(0, senior_churn.max() + 8)
plt.tight_layout()

plt.savefig(
    "python/churn_by_senior_citizen.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 13: Churn Rate by Partner Status - Slope Chart

partner_churn = (
    df.groupby("Partner")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

partner_labels = ["No", "Yes"]
partner_rates = [
    partner_churn.get("No", 0),
    partner_churn.get("Yes", 0)
]

plt.figure(figsize=(8, 5))

plt.plot(
    partner_labels,
    partner_rates,
    marker="o",
    markersize=12,
    linewidth=3,
    color="teal"
)

for label, rate in zip(partner_labels, partner_rates):
    plt.text(
        label,
        rate + 1,
        f"{rate:.2f}%",
        ha="center",
        fontsize=11
    )

plt.title("Customer Churn Rate by Partner Status")
plt.xlabel("Has a Partner?")
plt.ylabel("Churn Rate (%)")
plt.ylim(0, max(partner_rates) + 8)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    "python/churn_by_partner_status.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 14: Customer Churn Rate by Dependents

dependents_churn = (
    df.groupby("Dependents")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .sort_values()
)

plt.figure(figsize=(8, 5))

plt.hlines(
    y=dependents_churn.index,
    xmin=0,
    xmax=dependents_churn.values,
    color="slateblue",
    linewidth=3
)

plt.scatter(
    dependents_churn.values,
    dependents_churn.index,
    color="darkorange",
    s=160,
    zorder=3
)

for label, rate in dependents_churn.items():
    plt.text(
        rate + 0.5,
        label,
        f"{rate:.2f}%",
        va="center"
    )

plt.title("Customer Churn Rate by Dependents")
plt.xlabel("Churn Rate (%)")
plt.ylabel("Has Dependents?")
plt.xlim(0, dependents_churn.max() + 8)
plt.tight_layout()

plt.savefig(
    "python/churn_by_dependents.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 15: Churn Rate by Partner and Dependents

partner_dependents = df.pivot_table(
    index="Partner",
    columns="Dependents",
    values="Churn",
    aggfunc=lambda x: (x == "Yes").mean() * 100
)

plt.figure(figsize=(8, 5))

sns.heatmap(
    partner_dependents,
    annot=True,
    fmt=".2f",
    cmap="YlOrRd",
    linewidths=1,
    cbar_kws={"label": "Churn Rate (%)"}
)

plt.title("Customer Churn Rate by Partner and Dependents")
plt.xlabel("Has Dependents?")
plt.ylabel("Has a Partner?")
plt.tight_layout()

plt.savefig(
    "python/churn_by_partner_dependents.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 16: Churn Rate by Payment Method

payment_rate = (
    df.groupby("PaymentMethod")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.hlines(
    y=payment_rate.index,
    xmin=0,
    xmax=payment_rate.values,
    color="#B8C7D9",
    linewidth=3
)

plt.scatter(
    payment_rate.values,
    payment_rate.index,
    color="#E76F51",
    s=120,
    zorder=3
)

for method, rate in payment_rate.items():
    plt.text(
        rate + 0.5,
        method,
        f"{rate:.2f}%",
        va="center"
    )

plt.title("Customer Churn Rate by Payment Method")
plt.xlabel("Churn Rate (%)")
plt.ylabel("Payment Method")
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "python/churn_rate_by_payment_method.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 17: Customer Tenure Distribution by Churn Status

plt.figure(figsize=(9, 6))

sns.violinplot(
    data=df,
    x="Churn",
    y="tenure",
    hue="Churn",
    inner="quartile",
    palette="Set2",
    legend=False
)

plt.title("Customer Tenure Distribution by Churn Status")
plt.xlabel("Customer Churn")
plt.ylabel("Tenure (Months)")
plt.tight_layout()

plt.savefig(
    "python/tenure_violin_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 18: Total Charges by Churn Status

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="Churn",
    y="TotalCharges",
    hue="Churn",
    palette="Set2",
    legend=False
)

plt.title("Total Charges by Customer Churn Status")
plt.xlabel("Customer Churn")
plt.ylabel("Total Charges")
plt.tight_layout()

plt.savefig(
    "python/total_charges_by_churn.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 19: Correlation Heatmap

numeric_df = df[
    ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]
].copy()

# Convert columns to numeric values
for col in numeric_df.columns:
    numeric_df[col] = pd.to_numeric(numeric_df[col], errors="coerce")

# Calculate correlation
correlation_matrix = numeric_df.corr()

# Create heatmap
plt.figure(figsize=(9, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5,
    vmin=-1,
    vmax=1,
    center=0
)

plt.title("Correlation Between Numerical Customer Features")
plt.tight_layout()

plt.savefig(
    "python/correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 20: Monthly Charges Distribution by Churn Status

plt.figure(figsize=(10, 6))

sns.violinplot(
    data=df,
    x="Churn",
    y="MonthlyCharges",
    hue="Churn",
    palette={"No": "#2A9D8F", "Yes": "#E76F51"},
    inner="quartile",
    legend=False
)

plt.title("Monthly Charges Distribution by Churn Status")
plt.xlabel("Customer Churn")
plt.ylabel("Monthly Charges")
plt.tight_layout()

plt.savefig(
    "python/monthly_charges_churn_violin.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 21: Churn Rate by Tenure Group

tenure_bins = [0, 12, 24, 36, 48, 60, 72]
tenure_labels = [
    "0–12 months",
    "13–24 months",
    "25–36 months",
    "37–48 months",
    "49–60 months",
    "61–72 months"
]

df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=tenure_bins,
    labels=tenure_labels,
    include_lowest=True
)

tenure_churn = (
    df.groupby("TenureGroup", observed=False)["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

plt.figure(figsize=(10, 6))

plt.plot(
    tenure_churn.index.astype(str),
    tenure_churn.values,
    marker="o",
    markersize=8,
    linewidth=2.5,
    color="#E76F51"
)

for i, value in enumerate(tenure_churn.values):
    plt.annotate(
        f"{value:.1f}%",
        (i, value),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center"
    )

plt.title("Customer Churn Rate by Tenure Group")
plt.xlabel("Customer Tenure")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=25)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    "python/churn_rate_by_tenure_group.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Chart 22: Churn Rate by Contract and Internet Service

churn_comparison = (
    df.groupby(
        ["Contract", "InternetService"],
        observed=True
    )["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .reset_index(name="ChurnRate")
)

plt.figure(figsize=(11, 6))

sns.barplot(
    data=churn_comparison,
    x="Contract",
    y="ChurnRate",
    hue="InternetService",
    palette="Set2"
)

plt.title("Churn Rate by Contract Type and Internet Service")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate (%)")
plt.legend(title="Internet Service")
plt.tight_layout()

plt.savefig(
    "python/churn_contract_internet.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 23: Churn Rate by Payment Method

payment_churn_rate = (
    df.groupby("PaymentMethod")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.hlines(
    y=payment_churn_rate.index,
    xmin=0,
    xmax=payment_churn_rate.values,
    color="#A8DADC",
    linewidth=3
)

plt.scatter(
    payment_churn_rate.values,
    payment_churn_rate.index,
    color="#E76F51",
    s=120,
    zorder=3
)

for method, rate in payment_churn_rate.items():
    plt.text(
        rate + 0.5,
        method,
        f"{rate:.1f}%",
        va="center"
    )

plt.title("Customer Churn Rate by Payment Method")
plt.xlabel("Churn Rate (%)")
plt.ylabel("Payment Method")
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "python/churn_rate_by_payment_method.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 24: Churn Rate by Internet Service

internet_churn = (
    df.groupby("InternetService")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .sort_values()
)

plt.figure(figsize=(9, 5))

bars = plt.barh(
    internet_churn.index,
    internet_churn.values,
    color=["#2A9D8F", "#E9C46A", "#E76F51"]
)

for bar in bars:
    width = bar.get_width()
    plt.text(
        width + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.1f}%",
        va="center"
    )

plt.title("Customer Churn Rate by Internet Service")
plt.xlabel("Churn Rate (%)")
plt.ylabel("Internet Service")
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "python/churn_rate_by_internet_service.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
