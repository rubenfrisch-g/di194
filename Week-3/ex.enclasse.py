import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")

print(tips.shape)
print(tips.columns)

# Missing values
print(tips.isna().sum())

# 1
print(tips.groupby("day")["tip"].sum())

# 2
print(tips.groupby("time")["tip"].mean())

# 3
print(tips.groupby("size")["tip"].mean())

# 4
tips = tips.dropna()