"""
Titanic Dataset - Data Preprocessing Exercises (1 to 7)
Dataset: https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer


# ─────────────────────────────────────────────────────────────────────────────
# Load dataset
# ─────────────────────────────────────────────────────────────────────────────
df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
print("Dataset loaded:", df.shape)
print(df.head())


# ─────────────────────────────────────────────────────────────────────────────
# 🌟 Exercise 1: Duplicate Detection and Removal
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EXERCISE 1 - Duplicate Detection and Removal")
print("="*60)

rows_before = len(df)
print(f"Rows before: {rows_before}")

num_duplicates = df.duplicated().sum()
print(f"Duplicate rows found: {num_duplicates}")

df = df.drop_duplicates()

rows_after = len(df)
print(f"Rows after: {rows_after}")
print(f"Rows removed: {rows_before - rows_after}")


# ─────────────────────────────────────────────────────────────────────────────
# 🌟 Exercise 2: Handling Missing Values
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EXERCISE 2 - Handling Missing Values")
print("="*60)

print("\nMissing values per column:")
print(df.isnull().sum())

# --- Age: impute with median using SimpleImputer ---
imputer = SimpleImputer(strategy="median")
df["Age"] = imputer.fit_transform(df[["Age"]])
print(f"\nAge → imputed with median ({df['Age'].median():.1f})")

# --- Embarked: fill with most frequent value (mode) ---
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
print(f"Embarked → filled with mode ('{df['Embarked'].mode()[0]}')")

# --- Cabin: too many missing values (~77%) → drop the column ---
df = df.drop(columns=["Cabin"])
print("Cabin → dropped (>77% missing)")

print("\nRemaining missing values:")
print(df.isnull().sum())


# ─────────────────────────────────────────────────────────────────────────────
# 🌟 Exercise 3: Feature Engineering
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EXERCISE 3 - Feature Engineering")
print("="*60)

# --- Family Size ---
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1  # +1 for the passenger themselves
print("FamilySize created (SibSp + Parch + 1):")
print(df["FamilySize"].value_counts().head())

# --- Title extracted from Name ---
df["Title"] = df["Name"].str.extract(r",\s*([^\.]+)\.")
print("\nRaw titles found:")
print(df["Title"].value_counts())

# Simplify rare titles
rare_titles = ["Lady", "Countess", "Capt", "Col", "Don", "Dr",
               "Major", "Rev", "Sir", "Jonkheer", "Dona", "the Countess"]
df["Title"] = df["Title"].str.strip()
df["Title"] = df["Title"].replace(rare_titles, "Rare")
df["Title"] = df["Title"].replace({"Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"})
print("\nSimplified titles:")
print(df["Title"].value_counts())

# --- Label Encoding for Title ---
le = LabelEncoder()
df["TitleEncoded"] = le.fit_transform(df["Title"])
print("\nTitleEncoded (label encoding):")
print(dict(zip(le.classes_, le.transform(le.classes_))))


# ─────────────────────────────────────────────────────────────────────────────
# 🌟 Exercise 4: Outlier Detection and Handling
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EXERCISE 4 - Outlier Detection and Handling")
print("="*60)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Outlier Detection - Before Treatment", fontsize=14)

df["Fare"].plot(kind="box", ax=axes[0][0], title="Fare (before)")
df["Age"].plot(kind="box", ax=axes[0][1], title="Age (before)")
df["Fare"].plot(kind="hist", bins=40, ax=axes[1][0], title="Fare distribution (before)")
df["Age"].plot(kind="hist", bins=30, ax=axes[1][1], title="Age distribution (before)")
plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/outliers_before.png", dpi=100)
plt.close()

# --- IQR method on Fare ---
Q1 = df["Fare"].quantile(0.25)
Q3 = df["Fare"].quantile(0.75)
IQR = Q3 - Q1
fare_lower = Q1 - 1.5 * IQR
fare_upper = Q3 + 1.5 * IQR
print(f"\nFare IQR bounds: [{fare_lower:.2f}, {fare_upper:.2f}]")
print(f"Fare outliers (IQR): {((df['Fare'] < fare_lower) | (df['Fare'] > fare_upper)).sum()}")

# --- Z-score method on Age ---
z_scores = (df["Age"] - df["Age"].mean()) / df["Age"].std()
print(f"Age outliers (|Z| > 3): {(z_scores.abs() > 3).sum()}")

# --- Strategy 1: Quantile capping for Fare ---
cap_upper = df["Fare"].quantile(0.98)
df["Fare_capped"] = df["Fare"].clip(upper=cap_upper)
print(f"\nFare quantile cap at 0.98 = {cap_upper:.2f}")

# --- Strategy 2: Log transformation for Fare ---
df["Fare_log"] = np.log1p(df["Fare"])  # log1p handles 0 safely
print(f"Fare log-transformed (log1p): min={df['Fare_log'].min():.2f}, max={df['Fare_log'].max():.2f}")

# --- Strategy 3: Row removal for extreme Age outliers ---
df_no_outliers = df[z_scores.abs() <= 3].copy()
print(f"Rows removed by Age Z-score: {len(df) - len(df_no_outliers)}")

# Keep the main df with capping applied
df["Fare"] = df["Fare_capped"]

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
df["Fare"].plot(kind="box", ax=axes[0], title="Fare (after capping)")
df["Fare_log"].plot(kind="box", ax=axes[1], title="Fare (log transformed)")
plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/outliers_after.png", dpi=100)
plt.close()
print("\nOutlier visualizations saved.")


# ─────────────────────────────────────────────────────────────────────────────
# 🌟 Exercise 5: Data Standardization and Normalization
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EXERCISE 5 - Standardization and Normalization")
print("="*60)

# StandardScaler for Age (approximately normal after imputation)
scaler_std = StandardScaler()
df["Age_scaled"] = scaler_std.fit_transform(df[["Age"]])
print(f"Age → StandardScaler: mean={df['Age_scaled'].mean():.4f}, std={df['Age_scaled'].std():.4f}")

# MinMaxScaler for Fare (skewed distribution)
scaler_mm = MinMaxScaler()
df["Fare_normalized"] = scaler_mm.fit_transform(df[["Fare"]])
print(f"Fare → MinMaxScaler: min={df['Fare_normalized'].min():.4f}, max={df['Fare_normalized'].max():.4f}")

# MinMaxScaler for FamilySize (bounded integer)
df["FamilySize_normalized"] = scaler_mm.fit_transform(df[["FamilySize"]])
print(f"FamilySize → MinMaxScaler: min={df['FamilySize_normalized'].min():.4f}, max={df['FamilySize_normalized'].max():.4f}")


# ─────────────────────────────────────────────────────────────────────────────
# 🌟 Exercise 6: Feature Encoding
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EXERCISE 6 - Feature Encoding")
print("="*60)

# One-Hot Encoding for nominal variables: Sex and Embarked
sex_dummies = pd.get_dummies(df["Sex"], prefix="Sex", drop_first=True)
embarked_dummies = pd.get_dummies(df["Embarked"], prefix="Embarked")
title_dummies = pd.get_dummies(df["Title"], prefix="Title")

df = pd.concat([df, sex_dummies, embarked_dummies, title_dummies], axis=1)

# Drop original columns now replaced by encoded ones
df = df.drop(columns=["Sex", "Embarked", "Title"])

print("One-Hot Encoding applied to: Sex, Embarked, Title")
print("New encoded columns:", [c for c in df.columns if c.startswith(("Sex_", "Embarked_", "Title_"))])
print(f"\nDataset shape after encoding: {df.shape}")


# ─────────────────────────────────────────────────────────────────────────────
# 🌟 Exercise 7: Data Transformation for Age Feature
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EXERCISE 7 - Age Group Transformation")
print("="*60)

# Create age bins
bins = [0, 12, 18, 60, 100]
labels = ["Child", "Teen", "Adult", "Senior"]
df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)

print("Age group distribution:")
print(df["AgeGroup"].value_counts().sort_index())

# One-hot encode AgeGroup
age_group_dummies = pd.get_dummies(df["AgeGroup"], prefix="AgeGroup")
df = pd.concat([df, age_group_dummies], axis=1)
df = df.drop(columns=["AgeGroup"])

print("\nAgeGroup columns after encoding:")
print([c for c in df.columns if c.startswith("AgeGroup_")])
print(df[[c for c in df.columns if c.startswith("AgeGroup_")]].head())

# ─────────────────────────────────────────────────────────────────────────────
# Final Overview
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("FINAL DATASET OVERVIEW")
print("="*60)
print(f"Shape: {df.shape}")
print(f"\nColumns:\n{df.columns.tolist()}")
print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print("\nFirst rows:")
print(df.head())
