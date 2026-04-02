
# Exercise 1:
import scipy
print("SciPy version:", scipy.__version__)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm

# Exercise 2: 

data = [12, 15, 13, 12, 18, 20, 22, 21]

mean_value = np.mean(data)
median_value = np.median(data)
variance_value = np.var(data, ddof=1)   
std_value = np.std(data, ddof=1)      

print("Data:", data)
print("Mean:", mean_value)
print("Median:", median_value)
print("Variance:", variance_value)
print("Standard deviation:", std_value)


# Exercise 3:


x = np.linspace(10, 90, 500)
y = norm.pdf(x, loc=50, scale=10)

plt.figure(figsize=(8, 5))
plt.plot(x, y)
plt.title("Normal Distribution (mean=50, std=10)")
plt.xlabel("X")
plt.ylabel("Density")
plt.grid(True)
plt.show()


# Exercise 4: 


np.random.seed(42)
data1 = np.random.normal(50, 10, 100)
data2 = np.random.normal(60, 10, 100)

t_stat, p_value = stats.ttest_ind(data1, data2)

print("T-statistic:", t_stat)
print("P-value:", p_value)

if p_value < 0.05:
    print("The two groups are significantly different.")
else:
    print("The two groups are NOT significantly different.")


# Exercise 5: 

house_sizes = np.array([50, 70, 80, 100, 120])
house_prices = np.array([150000, 200000, 210000, 250000, 280000])

slope, intercept, r_value, p_value, std_err = stats.linregress(house_sizes, house_prices)

predicted_price_90 = slope * 90 + intercept

print("Slope:", slope)
print("Intercept:", intercept)
print("Predicted price for 90 square meters:", predicted_price_90)

print("\nInterpretation:")
print(f"The slope means that for each additional square meter, the house price increases by about {slope:.2f} currency units.")

plt.figure(figsize=(8, 5))
plt.scatter(house_sizes, house_prices, label="Data points")
plt.plot(house_sizes, slope * house_sizes + intercept, color="red", label="Regression line")
plt.title("Linear Regression: House Size vs Price")
plt.xlabel("House Size (m²)")
plt.ylabel("House Price")
plt.legend()
plt.grid(True)
plt.show()



# Exercise 6: 

fertilizer_1 = [5, 6, 7, 6, 5]
fertilizer_2 = [7, 8, 7, 9, 8]
fertilizer_3 = [4, 5, 4, 3, 4]

f_value, p_value = stats.f_oneway(fertilizer_1, fertilizer_2, fertilizer_3)

print("F-value:", f_value)
print("P-value:", p_value)

if p_value < 0.05:
    print("The fertilizers have significantly different effects on plant growth.")
else:
    print("The fertilizers do NOT have significantly different effects on plant growth.")

print("If the P-value were greater than 0.05, we would fail to reject the null hypothesis,")
print("which means we would conclude that there is no statistically significant difference between the fertilizers.")


# Exercise 7: 

n = 10
p = 0.5
k = 5

prob_5_heads = stats.binom.pmf(k, n, p)

print("Probability of getting exactly 5 heads in 10 coin flips:", prob_5_heads)

# Exercise 8:

print("Exercise 8")

data_corr = pd.DataFrame({
    'age': [23, 25, 30, 35, 40],
    'income': [35000, 40000, 50000, 60000, 70000]
})

pearson_corr, pearson_p = stats.pearsonr(data_corr["age"], data_corr["income"])
spearman_corr, spearman_p = stats.spearmanr(data_corr["age"], data_corr["income"])

print("Pearson correlation coefficient:", pearson_corr)
print("Pearson p-value:", pearson_p)
print("Spearman correlation coefficient:", spearman_corr)
print("Spearman p-value:", spearman_p)

print("\nInterpretation:")
print("Pearson measures linear correlation.")
print("Spearman measures monotonic rank correlation.")