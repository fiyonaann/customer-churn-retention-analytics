# Import libraries
import pandas as pd
import numpy as np

# 1. Load the original dataset
df = pd.read_csv("data/Telco-Customer-Churn.csv")

print("========== ORIGINAL DATASET ==========")
print("Dataset Shape:", df.shape)
print("\nFirst 5 Rows:")
print(df.head())

# 2. Check duplicate records
print("\n========== DUPLICATE CHECK ==========")
print("Duplicate Rows:", df.duplicated().sum())

# 3. Check missing values
print("\n========== MISSING VALUES BEFORE CLEANING ==========")
print(df.isnull().sum())

# 4. Clean column names
df.columns = df.columns.str.strip()

# 5. Remove unnecessary spaces from text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# 6. Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"].replace("", np.nan),
    errors="coerce"
)

# 7. Handle missing TotalCharges values
print("\n========== TOTAL CHARGES CLEANING ==========")

print("Missing TotalCharges before cleaning:",
      df["TotalCharges"].isnull().sum())

# Check whether missing charges belong to customers with zero tenure
zero_tenure_missing = (
    df["TotalCharges"].isnull() & (df["tenure"] == 0)
)

print("Missing charges with zero tenure:",
      zero_tenure_missing.sum())

# Replace missing charges with zero only for zero-tenure customers
df.loc[zero_tenure_missing, "TotalCharges"] = 0.0

# Stop if unexplained missing charges remain
if df["TotalCharges"].isnull().any():
    raise ValueError(
        "Missing TotalCharges values remain. "
        "Investigate these records before continuing."
    )

print("Missing TotalCharges after cleaning:",
      df["TotalCharges"].isnull().sum())

# 8. Remove duplicate records
duplicates_removed = df.duplicated().sum()
df = df.drop_duplicates()

print("\nDuplicate rows removed:", duplicates_removed)

# 9. Check missing values after cleaning
print("\n========== MISSING VALUES AFTER CLEANING ==========")
print(df.isnull().sum())

# 10. Display final dataset information
print("\n========== CLEANED DATASET SUMMARY ==========")
print("Dataset Shape:", df.shape)
print("Duplicate Rows:", df.duplicated().sum())
print("TotalCharges Data Type:", df["TotalCharges"].dtype)

print("\nFinal Data Types:")
print(df.dtypes)

# 11. Save the cleaned dataset
df.to_csv("data/cleaned_customer_churn.csv", index=False)

print("\n========== SUCCESS ==========")
print("Cleaned dataset saved to:")
print("data/cleaned_customer_churn.csv")
