import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# 1. Data Preparation
# =========================

# Generate random temperature data
# Values between -5°C and 35°C
# 10 cities and 12 months

temperature_data = np.random.uniform(-5, 35, size=(10, 12))


# Create city names

cities = [
    "City 1", "City 2", "City 3", "City 4", "City 5",
    "City 6", "City 7", "City 8", "City 9", "City 10"
]


# Create month names

months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]


# Convert NumPy array into a Pandas DataFrame

df = pd.DataFrame(
    temperature_data,
    index=cities,
    columns=months
)


print("Temperature Dataset:")
print(df)


# =========================
# 2. Data Analysis
# =========================

# Calculate annual average temperature for each city

annual_average = df.mean(axis=1)


print("\nAnnual Average Temperature:")
print(annual_average)


# Find hottest and coldest cities

highest_city = annual_average.idxmax()
lowest_city = annual_average.idxmin()


print("\nCity with highest average temperature:")
print(highest_city)


print("\nCity with lowest average temperature:")
print(lowest_city)


# =========================
# 3. Data Visualization
# =========================

plt.figure(figsize=(12, 6))


# Plot temperatures for each city

for city in df.index:
    plt.plot(
        months,
        df.loc[city],
        marker="o",
        label=city
    )


plt.title("Monthly Temperature Trends for Each City")

plt.xlabel("Month")

plt.ylabel("Temperature (°C)")

plt.legend()

plt.grid(True)

plt.show()


# =========================
# 4. Brief Report
# =========================

print("\nSummary Report:")

print(
    f"The city with the highest average temperature is {highest_city}."
)

print(
    f"The city with the lowest average temperature is {lowest_city}."
)

print(
    "The graph shows how temperatures change during the year for each city."
)