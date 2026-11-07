import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df = pd.read_csv("data/cleaned_customer_churn.csv")

# Services to analyze
services = [
    "PhoneService",
    "MultipleLines",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies"
]

# Calculate churn rate for each service
results = []

for service in services:
    churn_rate = (
        df.groupby(service)["Churn"]
        .apply(lambda x: (x == "Yes").mean() * 100)
    )

    for category, rate in churn_rate.items():
        results.append({
            "Service": service,
            "Category": category,
            "ChurnRate": rate
        })

results_df = pd.DataFrame(results)

# Display results
print("\n===== CHURN RATE BY CUSTOMER SERVICE =====")
print(results_df.round(2).to_string(index=False))

# Plot results
plt.figure(figsize=(13, 7))

sns.barplot(
    data=results_df,
    x="Service",
    y="ChurnRate",
    hue="Category"
)

plt.title("Customer Churn Rate by Service Subscription")
plt.xlabel("Customer Service")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Service Category")
plt.tight_layout()

plt.savefig(
    "service_churn_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
