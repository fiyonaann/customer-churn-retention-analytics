create database customer_churn_db;
select count(*) as total_customers from cleaned_customer_churn;
describe cleaned_customer_churn;

-- What is the overall customer churn rate?
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn;

-- Are customers with month-to-month contracts more likely to leave?
SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY Contract
ORDER BY churn_rate_percentage DESC;

-- Do customers using Fiber Optic internet churn more frequently than customers using DSL or no internet service?
SELECT
    InternetService,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY InternetService
ORDER BY churn_rate_percentage DESC;

-- Which payment method is associated with the highest customer churn?
SELECT
    PaymentMethod,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY PaymentMethod
ORDER BY churn_rate_percentage DESC;

-- Query 5: Customer churn by tenure group
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 Months'
        WHEN tenure <= 24 THEN '13-24 Months'
        WHEN tenure <= 48 THEN '25-48 Months'
        ELSE '49-72 Months'
    END AS tenure_group,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY tenure_group
ORDER BY MIN(tenure);

-- Query 6: Churn by contract type and internet service
SELECT
    Contract,
    InternetService,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY Contract, InternetService
ORDER BY churn_rate_percentage DESC;

-- Query 7: Churn by monthly charges
SELECT
    CASE
        WHEN MonthlyCharges < 35 THEN 'Low Charges'
        WHEN MonthlyCharges < 70 THEN 'Medium Charges'
        ELSE 'High Charges'
    END AS charge_category,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage,
    ROUND(AVG(MonthlyCharges), 2) AS average_monthly_charges
FROM cleaned_customer_churn
GROUP BY charge_category
ORDER BY churn_rate_percentage DESC;

-- Query 8: Churn by senior citizen status
SELECT
    CASE
        WHEN SeniorCitizen = 1 THEN 'Senior Citizen'
        ELSE 'Non-Senior Citizen'
    END AS customer_category,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY SeniorCitizen
ORDER BY churn_rate_percentage DESC;

-- Query 9: Churn by Online Security
SELECT
    OnlineSecurity,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY OnlineSecurity
ORDER BY churn_rate_percentage DESC;

-- Query 10: Customer Profile by Churn Status
SELECT
    Churn,
    COUNT(*) AS total_customers,
    ROUND(AVG(tenure), 2) AS average_tenure_months,
    ROUND(AVG(MonthlyCharges), 2) AS average_monthly_charges,
    ROUND(AVG(TotalCharges), 2) AS average_total_charges
FROM cleaned_customer_churn
GROUP BY Churn;

-- Query 11: Churn by Partner and Dependents
SELECT
    Partner,
    Dependents,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY Partner, Dependents
ORDER BY churn_rate_percentage DESC;

-- Query 12: Churn Rate by Customer Gender
SELECT
    gender,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY gender
ORDER BY churn_rate_percentage DESC;

-- Query 13: Churn by Paperless Billing
SELECT
    CASE
        WHEN PaperlessBilling = 'Yes' THEN 'Paperless Billing'
        WHEN PaperlessBilling = 'No' THEN 'Paper Billing'
    END AS billing_type,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY PaperlessBilling
ORDER BY churn_rate_percentage DESC;

-- Query 14: Churn by Paperless Billing with Clear Labels
SELECT
    CASE
        WHEN PaperlessBilling = 'Yes' THEN 'Paperless Billing'
        WHEN PaperlessBilling = 'No' THEN 'Traditional Paper Billing'
    END AS billing_type,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY PaperlessBilling
ORDER BY churn_rate_percentage DESC;

-- Query 15: Churn by Customer Tenure Category
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 Months'
        WHEN tenure <= 24 THEN '13-24 Months'
        WHEN tenure <= 48 THEN '25-48 Months'
        ELSE '49-72 Months'
    END AS tenure_category,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY tenure_category
ORDER BY MIN(tenure);

-- Churn by Internet Service with Clear Labels
SELECT
    CASE
        WHEN InternetService = 'DSL' THEN 'DSL Internet'
        WHEN InternetService = 'Fiber optic' THEN 'Fiber Optic Internet'
        ELSE 'No Internet Service'
    END AS internet_service_type,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY InternetService
ORDER BY churn_rate_percentage DESC;

-- Churn by Contract Type
SELECT
    CASE
        WHEN Contract = 'Month-to-month' THEN 'Monthly Contract'
        WHEN Contract = 'One year' THEN 'One-Year Contract'
        WHEN Contract = 'Two year' THEN 'Two-Year Contract'
    END AS contract_type,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY Contract
ORDER BY churn_rate_percentage DESC;

-- Churn by Monthly Charges Category
SELECT
    CASE
        WHEN MonthlyCharges < 35 THEN 'Low Monthly Charges'
        WHEN MonthlyCharges < 70 THEN 'Medium Monthly Charges'
        ELSE 'High Monthly Charges'
    END AS charges_category,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM cleaned_customer_churn
GROUP BY charges_category
ORDER BY churn_rate_percentage DESC;

-- Overall Customer Retention Summary
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS customers_lost,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS active_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS retention_rate_percentage,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage,
    ROUND(AVG(MonthlyCharges), 2) AS average_monthly_charges
FROM cleaned_customer_churn;