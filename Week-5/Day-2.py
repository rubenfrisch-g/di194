import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Exercise 1: Matrix Operations
# =========================

matrix = np.array([
    [1, 2, 3],
    [0, 1, 4],
    [5, 6, 0]
])

determinant = np.linalg.det(matrix)
inverse = np.linalg.inv(matrix)

print("Exercise 1")
print("Matrix:")
print(matrix)
print("Determinant:", determinant)
print("Inverse:")
print(inverse)
print("-" * 50)


# =========================
# Exercise 2: Statistical Analysis
# =========================

random_numbers = np.random.rand(50)

mean_value = np.mean(random_numbers)
median_value = np.median(random_numbers)
std_value = np.std(random_numbers)

print("Exercise 2")
print("Mean:", mean_value)
print("Median:", median_value)
print("Standard deviation:", std_value)
print("-" * 50)


# =========================
# Exercise 3: Date Manipulation
# =========================

dates = np.arange("2023-01-01", "2023-02-01", dtype="datetime64[D]")

formatted_dates = np.array([str(date).replace("-", "/") for date in dates])

print("Exercise 3")
print(formatted_dates)
print("-" * 50)


# =========================
# Exercise 4: Data Manipulation with NumPy and Pandas
# =========================

df = pd.DataFrame(
    np.random.randint(1, 100, size=(5, 4)),
    columns=["A", "B", "C", "D"]
)

print("Exercise 4")
print("DataFrame:")
print(df)

print("\nConditional selection: values in column A greater than 50")
print(df[df["A"] > 50])

print("\nSum:")
print(df.sum())

print("\nAverage:")
print(df.mean())
print("-" * 50)


# =========================
# Exercise 5: Image Representation
# =========================

# A grayscale image can be represented as a 2D NumPy array.
# Each value represents pixel intensity: 0 = black, 255 = white.

grayscale_image = np.array([
    [0, 50, 100, 150, 255],
    [0, 50, 100, 150, 255],
    [0, 50, 100, 150, 255],
    [0, 50, 100, 150, 255],
    [0, 50, 100, 150, 255]
])

print("Exercise 5")
print("5x5 grayscale image:")
print(grayscale_image)

plt.imshow(grayscale_image, cmap="gray")
plt.title("5x5 Grayscale Image")
plt.colorbar()
plt.show()
print("-" * 50)


# =========================
# Exercise 6: Basic Hypothesis Testing
# =========================

np.random.seed(0)

productivity_before = np.random.normal(loc=50, scale=10, size=30)
productivity_after = productivity_before + np.random.normal(loc=5, scale=3, size=30)

difference = productivity_after - productivity_before

mean_difference = np.mean(difference)

print("Exercise 6")
print("Hypothesis:")
print("H0: The training program does not improve productivity.")
print("H1: The training program improves productivity.")

print("\nMean productivity before:", np.mean(productivity_before))
print("Mean productivity after:", np.mean(productivity_after))
print("Mean improvement:", mean_difference)

if mean_difference > 0:
    print("Conclusion: Productivity improved after the training program.")
else:
    print("Conclusion: Productivity did not improve.")
print("-" * 50)


# =========================
# Exercise 7: Complex Array Comparison
# =========================

array1 = np.array([10, 25, 30, 45, 50])
array2 = np.array([12, 20, 30, 40, 60])

comparison = array1 > array2

print("Exercise 7")
print(comparison)
print("-" * 50)


# =========================
# Exercise 8: Time Series Data Manipulation
# =========================

dates_2023 = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

time_series = pd.DataFrame({
    "Date": dates_2023,
    "Value": np.random.randint(1, 100, len(dates_2023))
})

time_series = time_series.set_index("Date")

jan_mar = time_series["2023-01-01":"2023-03-31"]
apr_jun = time_series["2023-04-01":"2023-06-30"]
jul_sep = time_series["2023-07-01":"2023-09-30"]
oct_dec = time_series["2023-10-01":"2023-12-31"]

print("Exercise 8")
print("January to March:")
print(jan_mar.head())

print("\nApril to June:")
print(apr_jun.head())

print("\nJuly to September:")
print(jul_sep.head())

print("\nOctober to December:")
print(oct_dec.head())
print("-" * 50)


# =========================
# Exercise 9: Data Conversion
# =========================

numpy_array = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

df_from_array = pd.DataFrame(numpy_array, columns=["A", "B", "C"])

array_from_df = df_from_array.to_numpy()

print("Exercise 9")
print("NumPy array:")
print(numpy_array)

print("\nConverted to DataFrame:")
print(df_from_array)

print("\nConverted back to NumPy array:")
print(array_from_df)
print("-" * 50)


# =========================
# Exercise 10: Basic Visualization
# =========================

random_data = np.random.randint(1, 100, 10)

plt.plot(random_data, marker="o")
plt.title("Line Graph of Random Numbers")
plt.xlabel("Index")
plt.ylabel("Value")
plt.show()

print("Exercise 10 completed.")