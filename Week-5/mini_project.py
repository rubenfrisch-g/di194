# =========================================================
# MINI PROJECT : ADVANCED STATISTICAL ANALYSIS ON APPLE STOCK
# =========================================================

# =========================
# 1. DATA LOADING AND EXPLORATION
# =========================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
from scipy.signal import convolve

# Load dataset
df = pd.read_csv("Week-5/Apple Stock Prices (1981 to 2023).csv")

# Display first rows
print("First 5 rows:")
print(df.head())

# Dataset info
print("\nDataset info:")
print(df.info())

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Sort by date
df = df.sort_values("Date")

# Set date as index
df.set_index("Date", inplace=True)

print("\nData types:")
print(df.dtypes)

print("\nSummary statistics:")
print(df.describe())


# =========================
# 2. DATA VISUALIZATION
# =========================

# Closing price over time

plt.figure(figsize=(14,6))
plt.plot(df.index, df["Close"])
plt.title("Apple Closing Price Over Time")
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.show()


# Volume over time

plt.figure(figsize=(14,6))
plt.plot(df.index, df["Volume"])
plt.title("Trading Volume Over Time")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.show()


# High and Low prices

plt.figure(figsize=(14,6))

plt.plot(df.index, df["High"], label="High")
plt.plot(df.index, df["Low"], label="Low")

plt.title("High and Low Prices")
plt.xlabel("Date")
plt.ylabel("Price")

plt.legend()

plt.show()


# =========================
# 3. STATISTICAL ANALYSIS
# =========================

# Mean
print("\nMean values:")
print(df[["Open", "High", "Low", "Close", "Volume"]].mean())

# Median
print("\nMedian values:")
print(df[["Open", "High", "Low", "Close", "Volume"]].median())

# Standard deviation
print("\nStandard deviation:")
print(df[["Open", "High", "Low", "Close", "Volume"]].std())


# Moving average

df["MA_30"] = df["Close"].rolling(window=30).mean()

plt.figure(figsize=(14,6))

plt.plot(df.index, df["Close"], label="Close Price")
plt.plot(df.index, df["MA_30"], label="30-Day Moving Average")

plt.title("Closing Price and Moving Average")

plt.xlabel("Date")
plt.ylabel("Price")

plt.legend()

plt.show()


# =========================
# 4. HYPOTHESIS TESTING
# =========================

# Create year column
df["Year"] = df.index.year

# Compare average closing prices between two years

year1 = df[df["Year"] == 2020]["Close"]
year2 = df[df["Year"] == 2021]["Close"]

t_stat, p_value = stats.ttest_ind(year1, year2)

print("\nT-Test Results")
print("T-statistic:", t_stat)
print("P-value:", p_value)

if p_value < 0.05:
    print("There is a significant difference between the mean closing prices.")
else:
    print("There is no significant difference between the mean closing prices.")


# =========================
# DAILY RETURNS
# =========================

df["Daily_Return"] = df["Close"].pct_change()

# Remove NaN
returns = df["Daily_Return"].dropna()

# Plot returns distribution

plt.figure(figsize=(10,5))

sns.histplot(returns, bins=50, kde=True)

plt.title("Distribution of Daily Returns")

plt.show()


# Normality test

normality_test = stats.normaltest(returns)

print("\nNormality Test")
print("Statistic:", normality_test.statistic)
print("P-value:", normality_test.pvalue)

if normality_test.pvalue < 0.05:
    print("Returns are NOT normally distributed.")
else:
    print("Returns are normally distributed.")


# =========================
# 5. ADVANCED STATISTICAL TECHNIQUES
# =========================

# -------------------------
# Moving average with NumPy convolve
# -------------------------

window = 30

weights = np.ones(window) / window

moving_average = convolve(
    df["Close"],
    weights,
    mode="valid"
)

plt.figure(figsize=(14,6))

plt.plot(df.index, df["Close"], label="Close Price")

plt.plot(
    df.index[window-1:],
    moving_average,
    label="Convolve Moving Average"
)

plt.title("Moving Average using NumPy Convolve")

plt.legend()

plt.show()


# -------------------------
# Correlation analysis
# -------------------------

# Correlation between Close and Volume

correlation = np.corrcoef(
    df["Close"].dropna(),
    df["Volume"].dropna()
)

print("\nCorrelation Matrix:")
print(correlation)


# Correlation between moving average and volume

valid_volume = df["Volume"][window-1:]

corr_ma_volume = np.corrcoef(
    moving_average,
    valid_volume
)

print("\nCorrelation between Moving Average and Volume:")
print(corr_ma_volume)


# =========================
# 6. SUMMARY AND INSIGHTS
# =========================

print("\nSUMMARY")

print("""
- Apple stock prices generally increased over time.
- The moving average smooths short-term fluctuations and highlights long-term trends.
- Trading volume varies strongly across periods.
- Statistical testing showed whether closing prices changed significantly between years.
- Daily returns are often not perfectly normally distributed.
- Correlation analysis helps identify relationships between price evolution and trading volume.
""")


# =========================
# 7. REFLECTION
# =========================

print("\nREFLECTION")

print("""
Challenges:
- Handling time series data correctly.
- Understanding rolling averages and hypothesis testing.
- Managing NaN values created by percentage changes and moving averages.

Solutions:
- Converted dates using pandas datetime functions.
- Used rolling() and convolve() for trend analysis.
- Removed missing values with dropna() before statistical tests.
""")