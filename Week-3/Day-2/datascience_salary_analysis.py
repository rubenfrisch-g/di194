import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# ── Load dataset ──────────────────────────────────────────────────────────────
df = pd.read_csv('datascience_salaries.csv')

print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst rows:")
print(df.head())
print("\nExperience levels:")
print(df['experience_level'].value_counts())
print("\nSalary statistics:")
print(df['salary'].describe())

# =============================================================================
# TASK 1: Min-Max Normalization of Salary
# =============================================================================
print("\n" + "="*60)
print("TASK 1 — Min-Max Normalization of Salary")
print("="*60)

# Apply Min-Max normalization to scale salary between 0 and 1
# Formula: (x - min) / (max - min)
scaler = MinMaxScaler()
df['salary_normalized'] = scaler.fit_transform(df[['salary']])

print(f"Salary before normalization:")
print(f"  Min: ${df['salary'].min():,.0f}")
print(f"  Max: ${df['salary'].max():,.0f}")
print(f"  Mean: ${df['salary'].mean():,.0f}")

print(f"\nSalary after normalization:")
print(f"  Min: {df['salary_normalized'].min():.4f} (should be 0)")
print(f"  Max: {df['salary_normalized'].max():.4f} (should be 1)")
print(f"  Mean: {df['salary_normalized'].mean():.4f}")

# Visualize before and after normalization
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(df['salary'], bins=40, color='steelblue', edgecolor='white')
axes[0].set_title('Salary — Before Normalization')
axes[0].set_xlabel('Salary (USD)')
axes[0].set_ylabel('Count')

axes[1].hist(df['salary_normalized'], bins=40, color='coral', edgecolor='white')
axes[1].set_title('Salary — After Min-Max Normalization')
axes[1].set_xlabel('Normalized Salary [0, 1]')
axes[1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('salary_normalization.png', dpi=150)
plt.show()
print("Plot saved: salary_normalization.png")

# =============================================================================
# TASK 2: Dimensionality Reduction (PCA + t-SNE)
# =============================================================================
print("\n" + "="*60)
print("TASK 2 — Dimensionality Reduction")
print("="*60)

# Prepare numerical features for PCA
# We need to encode categorical columns first
df_encoded = df.copy()

# Encode categorical columns with LabelEncoder
le = LabelEncoder()
for col in ['job_title', 'job_type', 'experience_level', 'location', 'salary_currency']:
    df_encoded[col + '_encoded'] = le.fit_transform(df_encoded[col])

# Select only numerical columns for PCA
numerical_cols = ['job_title_encoded', 'job_type_encoded', 'experience_level_encoded',
                  'location_encoded', 'salary_currency_encoded', 'salary_normalized']

X = df_encoded[numerical_cols].values
print(f"Shape before PCA: {X.shape} ({X.shape[1]} features)")

# --- PCA ---
# PCA retains the most important information (variance) while reducing dimensions
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

print(f"\nPCA Results:")
print(f"  Shape after PCA: {X_pca.shape} (2 components)")
print(f"  Variance explained by PC1: {pca.explained_variance_ratio_[0]*100:.1f}%")
print(f"  Variance explained by PC2: {pca.explained_variance_ratio_[1]*100:.1f}%")
print(f"  Total variance retained: {sum(pca.explained_variance_ratio_)*100:.1f}%")

# Add PCA results to dataframe
df['PCA_1'] = X_pca[:, 0]
df['PCA_2'] = X_pca[:, 1]

# --- t-SNE ---
# t-SNE is better for visualizing clusters but slower than PCA
print("\nRunning t-SNE (this may take a moment)...")
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
X_tsne = tsne.fit_transform(X)

df['TSNE_1'] = X_tsne[:, 0]
df['TSNE_2'] = X_tsne[:, 1]
print(f"t-SNE shape: {X_tsne.shape}")

# Visualize PCA and t-SNE colored by experience level
colors = {'Senior': '#2196F3', 'Mid': '#4CAF50', 'Entry': '#FF9800', 'Executive': '#E91E63'}
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for level, color in colors.items():
    mask = df['experience_level'] == level
    axes[0].scatter(df.loc[mask, 'PCA_1'], df.loc[mask, 'PCA_2'],
                    c=color, label=level, alpha=0.6, s=30)
    axes[1].scatter(df.loc[mask, 'TSNE_1'], df.loc[mask, 'TSNE_2'],
                    c=color, label=level, alpha=0.6, s=30)

axes[0].set_title('PCA — 2 Components')
axes[0].set_xlabel('Principal Component 1')
axes[0].set_ylabel('Principal Component 2')
axes[0].legend()

axes[1].set_title('t-SNE — 2 Components')
axes[1].set_xlabel('t-SNE 1')
axes[1].set_ylabel('t-SNE 2')
axes[1].legend()

plt.tight_layout()
plt.savefig('dimensionality_reduction.png', dpi=150)
plt.show()
print("Plot saved: dimensionality_reduction.png")

# Scree plot — how much variance each PCA component explains
pca_full = PCA()
pca_full.fit(X)

plt.figure(figsize=(8, 4))
plt.bar(range(1, len(pca_full.explained_variance_ratio_) + 1),
        pca_full.explained_variance_ratio_ * 100, color='steelblue')
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained (%)')
plt.title('PCA Scree Plot — Variance per Component')
plt.tight_layout()
plt.savefig('pca_scree.png', dpi=150)
plt.show()
print("Plot saved: pca_scree.png")

# =============================================================================
# TASK 3: Aggregation by Experience Level
# =============================================================================
print("\n" + "="*60)
print("TASK 3 — Salary Aggregation by Experience Level")
print("="*60)

# Group by experience_level and calculate mean and median salary
salary_agg = df.groupby('experience_level')['salary'].agg(
    Average_Salary='mean',
    Median_Salary='median',
    Min_Salary='min',
    Max_Salary='max',
    Count='count'
).reset_index()

# Sort by average salary descending
salary_agg = salary_agg.sort_values('Average_Salary', ascending=False)

print("Salary statistics by experience level:")
print(salary_agg.to_string(index=False))

# Visualize average and median salary per experience level
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

exp_levels = salary_agg['experience_level']
x = range(len(exp_levels))

axes[0].bar(x, salary_agg['Average_Salary'], color='steelblue', width=0.4, label='Average')
axes[0].bar([i + 0.4 for i in x], salary_agg['Median_Salary'], color='coral', width=0.4, label='Median')
axes[0].set_xticks([i + 0.2 for i in x])
axes[0].set_xticklabels(exp_levels)
axes[0].set_title('Average vs Median Salary by Experience Level')
axes[0].set_ylabel('Salary (USD)')
axes[0].legend()
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Boxplot per experience level
df.boxplot(column='salary', by='experience_level', ax=axes[1],
           boxprops=dict(color='steelblue'),
           medianprops=dict(color='red', linewidth=2))
axes[1].set_title('Salary Distribution by Experience Level')
axes[1].set_xlabel('Experience Level')
axes[1].set_ylabel('Salary (USD)')
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.suptitle('')

plt.tight_layout()
plt.savefig('salary_by_experience.png', dpi=150)
plt.show()
print("Plot saved: salary_by_experience.png")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("\n" + "="*60)
print("FINAL SUMMARY")
print("="*60)
print("1. Min-Max Normalization: salary scaled from [30k-228k] to [0-1]")
print("2. PCA: 6 features reduced to 2 components")
print(f"   → PC1 explains {pca.explained_variance_ratio_[0]*100:.1f}% of variance")
print(f"   → PC2 explains {pca.explained_variance_ratio_[1]*100:.1f}% of variance")
print("3. t-SNE: alternative 2D projection for cluster visualization")
print("4. Salary aggregation by experience level:")
for _, row in salary_agg.iterrows():
    print(f"   {row['experience_level']:10s} → Avg: ${row['Average_Salary']:>8,.0f} | Median: ${row['Median_Salary']:>8,.0f} | n={int(row['Count'])}")
