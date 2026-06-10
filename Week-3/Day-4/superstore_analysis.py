import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# TASK 1: Data Scoping and Preparation
# =============================================================================
print("="*60)
print("TASK 1 — Data Scoping and Preparation")
print("="*60)

# Load dataset
df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')

print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
print("\nBasic info:")
print(df.dtypes)
print("\nDescriptive statistics:")
print(df[['Sales', 'Profit', 'Discount', 'Quantity']].describe())
print("\nMissing values:")
print(df.isnull().sum())

# --- Handle duplicates ---
print("\nDuplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()

# --- Handle missing values ---
if 'Postal Code' in df.columns:
    df['Postal Code'] = df['Postal Code'].fillna(0)

# --- Fix date types ---
date_columns = ['Order Date', 'Ship Date']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col])
print("\nDate types after conversion:")
print(df[date_columns].dtypes)

# --- Feature Engineering ---
df['Profit Margin']    = (df['Profit'] / df['Sales']) * 100
df['Order Year']       = df['Order Date'].dt.year
df['Order Month']      = df['Order Date'].dt.month
df['Order Month-Year'] = df['Order Date'].dt.to_period('M')

print("\nNew features sample:")
print(df[['Sales', 'Profit', 'Profit Margin', 'Order Year', 'Order Month']].head())

# =============================================================================
# TASK 2: Deep-Dive Exploratory Analysis (Matplotlib)
# =============================================================================
print("\n" + "="*60)
print("TASK 2 — Exploratory Analysis (Matplotlib)")
print("="*60)

# Prepare monthly sales data
monthly_sales = df.groupby(['Order Month-Year', 'Category'])['Sales'].sum().reset_index()
monthly_sales['Date'] = monthly_sales['Order Month-Year'].dt.to_timestamp()

# ── Time series: All categories ───────────────────────────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Overall monthly sales
total_monthly = df.groupby('Order Month-Year')['Sales'].sum()
axes[0].plot(total_monthly.index.to_timestamp(), total_monthly.values,
             marker='o', linewidth=2, markersize=4, color='steelblue')
axes[0].set_title('Monthly Sales Trend — All Categories', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Sales ($)')
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(True, alpha=0.3)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Monthly sales per category
colors = {'Furniture': '#E74C3C', 'Office Supplies': '#3498DB', 'Technology': '#2ECC71'}
for category, color in colors.items():
    cat_data = monthly_sales[monthly_sales['Category'] == category]
    axes[1].plot(cat_data['Date'], cat_data['Sales'],
                 marker='o', linewidth=2, markersize=3, label=category, color=color)

axes[1].set_title('Monthly Sales Trend by Category', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Sales ($)')
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True, alpha=0.3)
axes[1].legend()
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('time_series_sales.png', dpi=150)
plt.show()
print("Plot saved: time_series_sales.png")

# ── Geographic Sales Performance ──────────────────────────────────────────────
state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=True)

# Top 15 states
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

top_15 = state_sales.tail(15)
bars = axes[0].barh(range(len(top_15)), top_15.values, color='steelblue')
axes[0].set_yticks(range(len(top_15)))
axes[0].set_yticklabels(top_15.index)
axes[0].set_xlabel('Total Sales ($)')
axes[0].set_title('Top 15 States by Sales Performance', fontsize=13, fontweight='bold')
for i, (state, value) in enumerate(top_15.items()):
    axes[0].text(value + max(top_15.values) * 0.01, i, f'${value:,.0f}', va='center', fontsize=9)
axes[0].grid(axis='x', alpha=0.3)
axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Bottom 15 states
bottom_15 = state_sales.head(15)
axes[1].barh(range(len(bottom_15)), bottom_15.values, color='coral')
axes[1].set_yticks(range(len(bottom_15)))
axes[1].set_yticklabels(bottom_15.index)
axes[1].set_xlabel('Total Sales ($)')
axes[1].set_title('Bottom 15 States by Sales Performance', fontsize=13, fontweight='bold')
for i, (state, value) in enumerate(bottom_15.items()):
    axes[1].text(value + max(bottom_15.values) * 0.01, i, f'${value:,.0f}', va='center', fontsize=9)
axes[1].grid(axis='x', alpha=0.3)
axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('geographic_sales.png', dpi=150)
plt.show()
print("Plot saved: geographic_sales.png")

print(f"\nTotal states analyzed: {len(state_sales)}")
print(f"Top 5 states represent: {(state_sales.tail(5).sum()/df['Sales'].sum())*100:.1f}% of sales")

# =============================================================================
# TASK 3: Communicating Insights (Seaborn)
# =============================================================================
print("\n" + "="*60)
print("TASK 3 — Communicating Insights (Seaborn)")
print("="*60)

# ── Top 10 Most Profitable Products ───────────────────────────────────────────
product_profit = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 8))
ax = sns.barplot(x=product_profit.values, y=product_profit.index,
                 palette='viridis', orient='h')

plt.title('Top 10 Most Profitable Products\nExecutive Summary — Product Performance Analysis',
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Total Profit ($)', fontsize=12, fontweight='bold')
plt.ylabel('Product Name', fontsize=12, fontweight='bold')

for i, (product, profit) in enumerate(product_profit.items()):
    ax.text(profit + max(product_profit.values) * 0.01, i,
            f'${profit:,.0f}', va='center', fontweight='bold', fontsize=10)

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('top_products.png', dpi=150)
plt.show()
print("Plot saved: top_products.png")

print("\nKey Insights:")
print(f"  Most profitable product: ${product_profit.iloc[0]:,.0f}")
print(f"  Top 10 products contribute: ${product_profit.sum():,.0f} total profit")
print(f"  Average profit per top product: ${product_profit.mean():,.0f}")

# ── Discount vs Profit Scatter Plot ───────────────────────────────────────────
plt.figure(figsize=(14, 8))

sns.scatterplot(data=df, x='Discount', y='Profit', hue='Category', alpha=0.5, s=40)
sns.regplot(data=df, x='Discount', y='Profit', scatter=False,
            color='red', line_kws={'linewidth': 2, 'linestyle': '--'}, label='Overall trend')

plt.title('Discount Strategy Analysis: Impact on Profitability by Category',
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Discount Rate', fontsize=12, fontweight='bold')
plt.ylabel('Profit ($)', fontsize=12, fontweight='bold')
plt.axhline(y=0, color='black', linestyle='-', alpha=0.4, linewidth=1)
plt.text(0.52, 60, 'Break-even line', fontsize=10, alpha=0.6)
plt.grid(True, alpha=0.3)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('discount_vs_profit.png', dpi=150)
plt.show()
print("Plot saved: discount_vs_profit.png")

print("\nDiscount Analysis Insights:")
high_discount = df[df['Discount'] > 0.2]
print(f"  Transactions with >20% discount: {len(high_discount):,}")
print(f"  Average profit for high discounts: ${high_discount['Profit'].mean():.2f}")
print(f"  % of high-discount sales with losses: {(high_discount['Profit'] < 0).mean()*100:.1f}%")

print("\nCategory-specific discount impact:")
for category in df['Category'].unique():
    cat_data = df[df['Category'] == category]
    high_disc_cat = cat_data[cat_data['Discount'] > 0.2]
    if len(high_disc_cat) > 0:
        avg_loss = high_disc_cat['Profit'].mean()
        print(f"  {category}: avg profit at >20% discount = ${avg_loss:.2f}")

# =============================================================================
# TASK 4: Methodology and Tooling Review
# =============================================================================
print("\n" + "="*60)
print("TASK 4 — Matplotlib vs Seaborn Comparison")
print("="*60)

print("MATPLOTLIB STRENGTHS:")
print("  • Fine-grained control over every plot element")
print("  • Custom annotations and text positioning")
print("  • Precise subplot layouts and figure sizing")
print("  • Great for time-series and interactive widgets")

print("\nSEABORN STRENGTHS:")
print("  • Built-in statistical visualizations (regplot, boxplot...)")
print("  • Automatic color palettes and legends")
print("  • Clean, publication-ready default styling")
print("  • Easy categorical data visualization")

print("\nSPEED COMPARISON:")
start = time.time()
fig, ax = plt.subplots()
ax.plot(df.groupby('Order Year')['Sales'].sum())
plt.close()
matplotlib_time = time.time() - start

start = time.time()
fig, ax = plt.subplots()
sns.lineplot(data=df.groupby('Order Year')['Sales'].sum().reset_index(),
             x='Order Year', y='Sales', ax=ax)
plt.close()
seaborn_time = time.time() - start

print(f"  Matplotlib basic plot: {matplotlib_time:.4f}s")
print(f"  Seaborn equivalent:    {seaborn_time:.4f}s")

print("""
RECOMMENDATION:
  → Use Matplotlib for rapid exploration and fine control.
  → Use Seaborn for stakeholder-facing, publication-ready visuals.
""")

# =============================================================================
# TASK 5: Executive Summary + Dashboard
# =============================================================================
print("\n" + "="*60)
print("TASK 5 — Executive Summary & Dashboard")
print("="*60)

total_sales  = df['Sales'].sum()
total_profit = df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100

print("=== EXECUTIVE SUMMARY — KEY FINDINGS ===\n")
print(f"BUSINESS PERFORMANCE:")
print(f"  Total Revenue:        ${total_sales:,.0f}")
print(f"  Total Profit:         ${total_profit:,.0f}")
print(f"  Overall Profit Margin: {profit_margin:.1f}%")

top_state       = state_sales.index[-1]
top_state_sales = state_sales.iloc[-1]
print(f"\nGEOGRAPHIC PERFORMANCE:")
print(f"  Top state: {top_state} (${top_state_sales:,.0f})")
print(f"  Top 5 states = {(state_sales.tail(5).sum()/total_sales)*100:.1f}% of total sales")

top_category = df.groupby('Category')['Sales'].sum().sort_values(ascending=False).index[0]
print(f"\nPRODUCT PERFORMANCE:")
print(f"  Leading category: {top_category}")
print(f"  Most profitable product: {product_profit.index[0]}")

high_disc_loss = (df[df['Discount'] > 0.2]['Profit'] < 0).mean() * 100
print(f"\nDISCOUNT STRATEGY INSIGHTS:")
print(f"  {high_disc_loss:.1f}% of >20% discounts result in losses")
print(f"  Recommended max discount threshold: 20%")

# ── Full Dashboard ─────────────────────────────────────────────────────────────
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('US Superstore — Business Intelligence Dashboard', fontsize=16, fontweight='bold')

# 1. Monthly sales trend
monthly_total = df.groupby('Order Month-Year')['Sales'].sum()
ax1.plot(monthly_total.index.to_timestamp(), monthly_total.values,
         marker='o', markersize=3, linewidth=1.5, color='steelblue')
ax1.set_title('Monthly Sales Trend')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# 2. Category performance
category_sales = df.groupby('Category')['Sales'].sum()
bars = ax2.bar(category_sales.index, category_sales.values,
               color=['#E74C3C', '#3498DB', '#2ECC71'])
ax2.set_title('Sales by Category')
ax2.set_ylabel('Sales ($)')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars, category_sales.values):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 5000,
             f'${val:,.0f}', ha='center', fontsize=10)

# 3. Top 10 states
top_10 = state_sales.tail(10)
ax3.barh(range(len(top_10)), top_10.values, color='mediumpurple')
ax3.set_yticks(range(len(top_10)))
ax3.set_yticklabels(top_10.index)
ax3.set_title('Top 10 States by Sales')
ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# 4. Discount vs Profit
for category in df['Category'].unique():
    cat_data = df[df['Category'] == category]
    ax4.scatter(cat_data['Discount'], cat_data['Profit'], label=category, alpha=0.5, s=15)
ax4.set_xlabel('Discount')
ax4.set_ylabel('Profit ($)')
ax4.set_title('Discount vs Profit by Category')
ax4.legend()
ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('superstore_dashboard.png', dpi=150)
plt.show()
print("\nDashboard saved: superstore_dashboard.png")

# ── Outlier Annotation ─────────────────────────────────────────────────────────
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='Discount', y='Profit', hue='Category', alpha=0.5, s=40)

top_3    = df.nlargest(3, 'Profit')
bottom_3 = df.nsmallest(3, 'Profit')

for _, row in top_3.iterrows():
    plt.annotate(f'Best: ${row["Profit"]:.0f}',
                 xy=(row['Discount'], row['Profit']),
                 xytext=(15, 5), textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.8),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'), fontsize=9)

for _, row in bottom_3.iterrows():
    plt.annotate(f'Worst: ${row["Profit"]:.0f}',
                 xy=(row['Discount'], row['Profit']),
                 xytext=(15, -15), textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='lightsalmon', alpha=0.8),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'), fontsize=9)

plt.axhline(y=0, color='black', linestyle='--', alpha=0.4)
plt.title('Discount vs Profit — Outlier Identification', fontsize=13, fontweight='bold')
plt.xlabel('Discount Rate')
plt.ylabel('Profit ($)')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('discount_outliers.png', dpi=150)
plt.show()
print("Plot saved: discount_outliers.png")

print("\n=== ANALYSIS COMPLETE ===")
print("Files generated:")
print("  • time_series_sales.png")
print("  • geographic_sales.png")
print("  • top_products.png")
print("  • discount_vs_profit.png")
print("  • superstore_dashboard.png")
print("  • discount_outliers.png")
