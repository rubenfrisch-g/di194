import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# =========================
# 1. Data Import and Cleaning
# =========================

df = pd.read_csv("Week-5/global_power_plant_database.csv")

print("First rows:")
print(df.head())

print("\nDataset info:")
print(df.info())

print("\nMissing values:")
print(df.isna().sum())

# Clean column names
df.columns = df.columns.str.strip()

# Convert relevant columns to numeric if they exist
numeric_columns = ["capacity_mw", "latitude", "longitude", "commissioning_year"]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Handle missing values
if "capacity_mw" in df.columns:
    df["capacity_mw"] = df["capacity_mw"].fillna(df["capacity_mw"].median())

if "primary_fuel" in df.columns:
    df["primary_fuel"] = df["primary_fuel"].fillna("Unknown")

if "country" in df.columns:
    df["country"] = df["country"].fillna("Unknown")

print("\nMissing values after cleaning:")
print(df.isna().sum())


# =========================
# 2. Exploratory Data Analysis
# =========================

print("\nSummary statistics:")
print(df.describe())

if "capacity_mw" in df.columns:
    print("\nMean capacity:", df["capacity_mw"].mean())
    print("Median capacity:", df["capacity_mw"].median())
    print("Standard deviation capacity:", df["capacity_mw"].std())

if "country" in df.columns:
    print("\nPower plants by country:")
    print(df["country"].value_counts().head(10))

if "primary_fuel" in df.columns:
    print("\nPower plants by fuel type:")
    print(df["primary_fuel"].value_counts())


# =========================
# 3. Statistical Analysis
# =========================

if "primary_fuel" in df.columns and "capacity_mw" in df.columns:
    print("\nAverage capacity by fuel type:")
    fuel_capacity = df.groupby("primary_fuel")["capacity_mw"].mean().sort_values(ascending=False)
    print(fuel_capacity)

    # Hypothesis testing between two most common fuel types
    top_fuels = df["primary_fuel"].value_counts().head(2).index

    fuel_1 = df[df["primary_fuel"] == top_fuels[0]]["capacity_mw"].dropna()
    fuel_2 = df[df["primary_fuel"] == top_fuels[1]]["capacity_mw"].dropna()

    t_stat, p_value = stats.ttest_ind(fuel_1, fuel_2, equal_var=False)

    print(f"\nT-test between {top_fuels[0]} and {top_fuels[1]}:")
    print("T-statistic:", t_stat)
    print("P-value:", p_value)

    if p_value < 0.05:
        print("Conclusion: The mean power output differs significantly between these fuel types.")
    else:
        print("Conclusion: No statistically significant difference was found.")


# =========================
# 4. Time Series Analysis
# =========================

if "commissioning_year" in df.columns:
    yearly_capacity = df.groupby("commissioning_year")["capacity_mw"].sum()

    print("\nTotal capacity by year:")
    print(yearly_capacity.tail())

    plt.figure(figsize=(10, 5))
    yearly_capacity.plot()
    plt.title("Total Power Capacity Over Time")
    plt.xlabel("Year")
    plt.ylabel("Total Capacity MW")
    plt.show()

    if "primary_fuel" in df.columns:
        fuel_trend = df.groupby(["commissioning_year", "primary_fuel"]).size().unstack(fill_value=0)

        fuel_trend.plot(figsize=(12, 6))
        plt.title("Evolution of Fuel Types Over Time")
        plt.xlabel("Year")
        plt.ylabel("Number of Power Plants")
        plt.show()


# =========================
# 5. Advanced Visualization
# =========================

if "primary_fuel" in df.columns:
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, y="primary_fuel", order=df["primary_fuel"].value_counts().index)
    plt.title("Distribution of Power Plants by Fuel Type")
    plt.xlabel("Count")
    plt.ylabel("Fuel Type")
    plt.show()

if "country" in df.columns:
    top_countries = df["country"].value_counts().head(10)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_countries.values, y=top_countries.index)
    plt.title("Top 10 Countries by Number of Power Plants")
    plt.xlabel("Number of Power Plants")
    plt.ylabel("Country")
    plt.show()

if "latitude" in df.columns and "longitude" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="longitude", y="latitude", hue="primary_fuel" if "primary_fuel" in df.columns else None)
    plt.title("Geographical Distribution of Power Plants")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()


# =========================
# 6. Matrix Operations
# =========================

matrix_columns = []

for col in ["capacity_mw", "latitude", "longitude"]:
    if col in df.columns:
        matrix_columns.append(col)

if len(matrix_columns) >= 2:
    matrix_data = df[matrix_columns].dropna().to_numpy()

    covariance_matrix = np.cov(matrix_data, rowvar=False)

    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    print("\nCovariance matrix:")
    print(covariance_matrix)

    print("\nEigenvalues:")
    print(eigenvalues)

    print("\nEigenvectors:")
    print(eigenvectors)

    print("\nInterpretation:")
    print("Eigenvalues show how much variance exists in each main direction of the data.")
    print("Eigenvectors show the directions in which attributes such as capacity and location vary together.")


# =========================
# 7. NumPy with Pandas and Matplotlib
# =========================

if "capacity_mw" in df.columns:
    capacity_array = df["capacity_mw"].to_numpy()

    high_capacity_filter = capacity_array > np.percentile(capacity_array, 90)

    high_capacity_plants = df[high_capacity_filter]

    print("\nTop 10% high-capacity power plants:")
    print(high_capacity_plants.head())

    plt.figure(figsize=(8, 5))
    plt.hist(np.log1p(capacity_array), bins=30)
    plt.title("Log-Transformed Distribution of Power Plant Capacity")
    plt.xlabel("log(1 + capacity_mw)")
    plt.ylabel("Frequency")
    plt.show()


# =========================
# Final Summary
# =========================

print("\nSummary:")
print("The dataset was cleaned, missing values were handled, and numerical columns were converted.")
print("Power plants were analyzed by country, fuel type, capacity, and time trends where available.")
print("Statistical tests were used to compare power output between fuel types.")
print("Visualizations helped identify differences in fuel distribution, geography, and power capacity.")