# Exercice 1

import pandas as pd 
import seaborn as sns 

titanic = pd.read_csv('Week-3/Day-2/train.csv')
duplicates = titanic.duplicated().sum()

print(f"Number of row: {duplicates}")

rows_before = len(titanic)
print(f"Rows before removing duplicates: {rows_before}")

titanic_clean = titanic.drop_duplicates()

row_after = len(titanic_clean)
print(f"Row after removing duplicates: {row_after}")

# Exercice 2

df = titanic.copy()
print(df.isna().sum())

df_drop = df.dropna(subset=['Age'])
print(df_drop)

df['Age'] = df['Age'].fillna(df['Age'].mean())

df['Embarked'] = df['Embarked'].fillna(('Unknown'))

# Exercice 3

df = titanic.copy()
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

df["Title"] = df["Name"].str.extract(r",\s*([^.]+)\.")

df_encoded = pd.get_dummies(df, columns=["Sex", "Embarked", "Title"], drop_first=True)

print(df_encoded.head())

# Exercice 4

sns.boxplot(x=df["Fare"])

Q1 = df["Fare"].quantile(0.25)
Q3 = df["Fare"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

cap = df["Fare"].quantile(0.98)
df["Fare"] = df["Fare"].clip(upper=cap)

# Exercice 6

df = pd.get_dummies(df, columns=["Sex", "Embarked"], drop_first=True)

# Exercice 7

bins = [0, 12, 18, 60, 100]
labels = ["Child", "Teen", "Adult", "Senior"]

df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels)

df = pd.get_dummies(df, columns=["AgeGroup"])