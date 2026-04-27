# =====================================================
# MOBILE PRICE CLASSIFICATION - DATA ANALYSIS PROJECT
# =====================================================

# =========================
# 1. Data Loading and Exploration
# =========================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

df = pd.read_csv("Week-5/train.csv")

print("First rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDescriptive statistics:")
print(df.describe())

print("\nTarget variable distribution:")
print(df["price_range"].value_counts())


# =========================
# 2. Data Cleaning and Preprocessing
# =========================

# Check duplicates
print("\nDuplicates:", df.duplicated().sum())

# Remove duplicates if any
df = df.drop_duplicates()

# Fill missing numeric values with median
for col in df.columns:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# In this dataset, most variables are already numerical.
# If categorical columns existed, we would use pd.get_dummies().
print("\nAll columns are ready for numerical analysis.")


# =========================
# 3. Statistical Analysis with NumPy and SciPy
# =========================

features = df.drop("price_range", axis=1)
target = df["price_range"]

print("\nStatistical Analysis for Each Feature")

for col in features.columns:
    print("\nFeature:", col)
    print("Mean:", np.mean(df[col]))
    print("Median:", np.median(df[col]))
    print("Mode:", stats.mode(df[col], keepdims=True).mode[0])
    print("Range:", np.max(df[col]) - np.min(df[col]))
    print("Variance:", np.var(df[col]))
    print("Standard Deviation:", np.std(df[col]))
    print("Skewness:", stats.skew(df[col]))
    print("Kurtosis:", stats.kurtosis(df[col]))


# =========================
# Hypothesis Testing
# =========================

# Example: compare RAM between low price phones and high price phones

low_price = df[df["price_range"] == 0]["ram"]
high_price = df[df["price_range"] == 3]["ram"]

t_stat, p_value = stats.ttest_ind(low_price, high_price, equal_var=False)

print("\nHypothesis Test: RAM in Low vs High Price Phones")
print("T-statistic:", t_stat)
print("P-value:", p_value)

if p_value < 0.05:
    print("Conclusion: RAM differs significantly between low and high price phones.")
else:
    print("Conclusion: No significant difference in RAM between the groups.")


# =========================
# Feature-Target Correlations
# =========================

print("\nCorrelation with price_range:")

correlations = {}

for col in features.columns:
    corr, p_val = stats.pearsonr(df[col], df["price_range"])
    correlations[col] = corr
    print(f"{col}: correlation = {corr:.3f}, p-value = {p_val:.5f}")

correlation_df = pd.DataFrame(
    list(correlations.items()),
    columns=["Feature", "Correlation"]
).sort_values(by="Correlation", ascending=False)

print("\nSorted correlations:")
print(correlation_df)


# =========================
# 4. Data Visualization with Matplotlib / Seaborn
# =========================

# Histogram of RAM
plt.figure(figsize=(8, 5))
plt.hist(df["ram"], bins=30)
plt.title("Distribution of RAM")
plt.xlabel("RAM")
plt.ylabel("Frequency")
plt.show()


# Boxplot: RAM by price range
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="price_range", y="ram")
plt.title("RAM by Price Range")
plt.xlabel("Price Range")
plt.ylabel("RAM")
plt.show()


# Scatter plot: RAM vs Battery Power
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="ram", y="battery_power", hue="price_range")
plt.title("RAM vs Battery Power by Price Range")
plt.xlabel("RAM")
plt.ylabel("Battery Power")
plt.show()


# Boxplot: Battery Power by Price Range
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="price_range", y="battery_power")
plt.title("Battery Power by Price Range")
plt.xlabel("Price Range")
plt.ylabel("Battery Power")
plt.show()


# Correlation heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(df.corr(), cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()


# Top correlations with price_range
plt.figure(figsize=(10, 6))
sns.barplot(data=correlation_df, x="Correlation", y="Feature")
plt.title("Feature Correlation with Price Range")
plt.xlabel("Correlation")
plt.ylabel("Feature")
plt.show()


# =========================
# 5. Insight Synthesis and Conclusion
# =========================

print("\nINSIGHTS AND CONCLUSION")

print("""
1. The dataset contains only numerical variables, so little categorical preprocessing is needed.

2. RAM is usually the strongest determinant of mobile phone price range.
   Higher RAM values are strongly associated with higher price categories.

3. Battery power, pixel resolution, and internal memory may also influence price,
   but their effects are generally weaker than RAM.

4. The hypothesis test comparing RAM between low-price and high-price phones
   shows whether the difference is statistically significant.

5. The visualizations confirm that price categories are not random:
   some technical specifications clearly increase with price range.

6. Unexpected findings may include features with weak correlation to price,
   meaning not every technical characteristic strongly affects price classification.
""")