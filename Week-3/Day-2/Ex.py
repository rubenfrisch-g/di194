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
