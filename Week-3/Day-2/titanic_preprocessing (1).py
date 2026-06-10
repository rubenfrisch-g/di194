import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from scipy import stats

# ── Load dataset ──────────────────────────────────────────────────────────────
df = pd.read_csv('train.csv')
print("Dataset shape:", df.shape)
print("\nFirst rows:")
print(df.head())

# =============================================================================
# EXERCISE 1: Duplicate Detection and Removal
# =============================================================================
print("\n" + "="*60)
print("EXERCISE 1 — Duplicate Detection and Removal")
print("="*60)

# Check rows before
print("Rows before:", len(df))

# Identify duplicates
duplicates = df.duplicated()
print("Number of duplicate rows:", duplicates.sum())

# Remove duplicates
df = df.drop_duplicates()

# Verify removal
print("Rows after:", len(df))
# The Titanic dataset is already clean — no duplicates expected

# =============================================================================
# EXERCISE 2: Handling Missing Values
# =============================================================================
print("\n" + "="*60)
print("EXERCISE 2 — Handling Missing Values")
print("="*60)

# Identify missing values
print("Missing values per column:")
print(df.isnull().sum())
print("\nPercentage missing:")
print((df.isnull().sum() / len(df) * 100).round(2))

# Strategy 1: Fill Age with median (robust to outliers)
# We use median instead of mean because Age can be skewed
df['Age'] = df['Age'].fillna(df['Age'].median())
print("\nAge missing after fillna:", df['Age'].isnull().sum())

# Strategy 2: Fill Embarked with most frequent value (mode)
# Only 2 missing values — filling with mode is reasonable
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
print("Embarked missing after fillna:", df['Embarked'].isnull().sum())

# Strategy 3: Drop Cabin column — 77% missing, not worth imputing
df = df.drop(columns=['Cabin'])
print("Cabin column dropped.")

# Using SimpleImputer from sklearn as an alternative approach
imputer = SimpleImputer(strategy='median')
df[['Age']] = imputer.fit_transform(df[['Age']])
print("\nRemaining missing values:")
print(df.isnull().sum())

# =============================================================================
# EXERCISE 3: Feature Engineering
# =============================================================================
print("\n" + "="*60)
print("EXERCISE 3 — Feature Engineering")
print("="*60)

# Create FamilySize from SibSp + Parch + 1 (self)
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
print("FamilySize sample:")
print(df['FamilySize'].value_counts().head())

# Extract Title from Name column using regex
# Name format: 'Last, Title. First' — extract what's before the dot
df['Title'] = df['Name'].str.extract(r',\s*([^\.]+)\.')
print("\nTitles found:")
print(df['Title'].value_counts())

# Group rare titles into 'Rare' to reduce dimensionality
rare_titles = df['Title'].value_counts()[df['Title'].value_counts() < 10].index
df['Title'] = df['Title'].replace(rare_titles, 'Rare')
print("\nTitles after grouping:")
print(df['Title'].value_counts())

# Label encode the Title column
# We do NOT scale numerical features yet — that comes after outlier handling
le = LabelEncoder()
df['Title_encoded'] = le.fit_transform(df['Title'])
print("\nTitle encoding mapping:")
for i, cls in enumerate(le.classes_):
    print(f"  {cls} -> {i}")

# =============================================================================
# EXERCISE 4: Outlier Detection and Handling
# =============================================================================
print("\n" + "="*60)
print("EXERCISE 4 — Outlier Detection and Handling")
print("="*60)

# Visualize distributions of Fare and Age
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

df['Fare'].hist(ax=axes[0, 0], bins=50, color='steelblue')
axes[0, 0].set_title('Fare — Histogram')

df.boxplot(column='Fare', ax=axes[0, 1])
axes[0, 1].set_title('Fare — Boxplot')

df['Age'].hist(ax=axes[1, 0], bins=30, color='coral')
axes[1, 0].set_title('Age — Histogram')

df.boxplot(column='Age', ax=axes[1, 1])
axes[1, 1].set_title('Age — Boxplot')

plt.tight_layout()
plt.savefig('outliers_before.png')
plt.show()
print("Plot saved as outliers_before.png")

# IQR method for Fare
Q1 = df['Fare'].quantile(0.25)
Q3 = df['Fare'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers_fare = df[(df['Fare'] < lower) | (df['Fare'] > upper)]
print(f"\nFare outliers detected: {len(outliers_fare)}")
print(f"IQR bounds: [{lower:.2f}, {upper:.2f}]")

# Cap Fare at 98th percentile
cap_98 = df['Fare'].quantile(0.98)
print(f"Fare 98th percentile: {cap_98:.2f}")
df['Fare_capped'] = df['Fare'].clip(upper=cap_98)
print(f"Max Fare before: {df['Fare'].max():.2f}")
print(f"Max Fare after:  {df['Fare_capped'].max():.2f}")

# Log transformation for Fare
df['Fare_log'] = np.log1p(df['Fare'])  # log1p = log(1+x) to handle zeros

# Z-score method for Age
z_scores = np.abs(stats.zscore(df['Age']))
outliers_age = df[z_scores > 3]
print(f"\nAge outliers (Z-score > 3): {len(outliers_age)}")

# Cap Age at 98th percentile
cap_age = df['Age'].quantile(0.98)
df['Age'] = df['Age'].clip(upper=cap_age)
print(f"Age capped at: {cap_age:.2f}")

# =============================================================================
# EXERCISE 5: Data Standardization and Normalization
# =============================================================================
print("\n" + "="*60)
print("EXERCISE 5 — Standardization and Normalization")
print("="*60)

# StandardScaler for Age (roughly normally distributed) — mean=0, std=1
scaler_std = StandardScaler()
df['Age_scaled'] = scaler_std.fit_transform(df[['Age']])
print("Age after StandardScaler:")
print(f"  Mean: {df['Age_scaled'].mean():.4f} (should be ~0)")
print(f"  Std:  {df['Age_scaled'].std():.4f} (should be ~1)")

# MinMaxScaler for Fare (skewed) — scales to [0, 1]
scaler_mm = MinMaxScaler()
df['Fare_scaled'] = scaler_mm.fit_transform(df[['Fare_capped']])
print("\nFare after MinMaxScaler:")
print(f"  Min: {df['Fare_scaled'].min():.4f} (should be 0)")
print(f"  Max: {df['Fare_scaled'].max():.4f} (should be 1)")

# =============================================================================
# EXERCISE 6: Feature Encoding
# =============================================================================
print("\n" + "="*60)
print("EXERCISE 6 — Feature Encoding")
print("="*60)

# One-Hot Encoding for Sex (nominal variable)
sex_encoded = pd.get_dummies(df['Sex'], prefix='Sex', drop_first=True)
df = pd.concat([df, sex_encoded], axis=1)
print("Sex encoded columns:", sex_encoded.columns.tolist())

# One-Hot Encoding for Embarked (nominal: S, C, Q)
embarked_encoded = pd.get_dummies(df['Embarked'], prefix='Embarked', drop_first=True)
df = pd.concat([df, embarked_encoded], axis=1)
print("Embarked encoded columns:", embarked_encoded.columns.tolist())

# One-Hot Encoding for Title
title_encoded = pd.get_dummies(df['Title'], prefix='Title', drop_first=True)
df = pd.concat([df, title_encoded], axis=1)
print("Title encoded columns:", title_encoded.columns.tolist())

print("\nDataset shape after all encodings:", df.shape)

# =============================================================================
# EXERCISE 7: Data Transformation for Age Feature
# =============================================================================
print("\n" + "="*60)
print("EXERCISE 7 — Age Group Transformation")
print("="*60)

# Create age groups using pd.cut()
# Bins: child (0-12), teen (12-18), adult (18-60), senior (60+)
df['AgeGroup'] = pd.cut(
    df['Age'],
    bins=[0, 12, 18, 60, 100],
    labels=['Child', 'Teen', 'Adult', 'Senior']
)

print("Age group distribution:")
print(df['AgeGroup'].value_counts())

# One-Hot Encoding for AgeGroup using pd.get_dummies()
age_group_encoded = pd.get_dummies(df['AgeGroup'], prefix='AgeGroup', drop_first=True)
df = pd.concat([df, age_group_encoded], axis=1)
print("\nAgeGroup encoded columns:", age_group_encoded.columns.tolist())

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("\n" + "="*60)
print("PREPROCESSING SUMMARY")
print("="*60)
print("1. Duplicates    : none found")
print("2. Missing values: Age -> median, Embarked -> mode, Cabin -> dropped")
print("3. New features  : FamilySize, Title")
print("4. Outliers      : Fare and Age capped at 98th percentile")
print("5. Scaling       : Age -> StandardScaler, Fare -> MinMaxScaler")
print("6. Encoding      : Sex, Embarked, Title -> One-Hot Encoding")
print("7. Age groups    : Child/Teen/Adult/Senior -> One-Hot Encoding")
print(f"\nFinal dataset shape: {df.shape}")
print("\nFinal columns:")
print(df.columns.tolist())
