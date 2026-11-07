import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned_customer_churn.csv")

# Calculate revenue metrics by churn status
revenue_analysis = df.groupby("Churn").agg(
    Customer_Count=("customerID", "count"),
    Average_Monthly_Charges=("MonthlyCharges", "mean"),
    Total_Monthly_Revenue=("MonthlyCharges", "sum"),
    Average_Tenure=("tenure", "mean")
).round(2)

print("\n===== REVENUE ANALYSIS BY CHURN STATUS =====")
print(revenue_analysis)

# Calculate monthly revenue associated with churned customers
churned_revenue = df.loc[
    df["Churn"] == "Yes", "MonthlyCharges"
].sum()

total_revenue = df["MonthlyCharges"].sum()

print(
    f"\nMonthly revenue associated with churned customers: ${churned_revenue:,.2f}")
print(f"Total monthly revenue across all customers: ${total_revenue:,.2f}")

print(
    "Percentage of current monthly revenue associated with churned customers:",
    f"{(churned_revenue / total_revenue) * 100:.2f}%"
)
