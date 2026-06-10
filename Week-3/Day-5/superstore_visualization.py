import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# TASK 1: Data Preparation
# =============================================================================
print("="*60)
print("TASK 1 — Data Preparation")
print("="*60)

# Load dataset
df = pd.read_excel('US_Superstore_data.xls', engine='xlrd')

print("Dataset Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# --- Cleaning ---
df = df.drop_duplicates()
df['Postal Code'] = df['Postal Code'].fillna(0)

# --- Date columns already datetime from Excel ---
# Verify
print("\nDate columns:")
print(df[['Order Date', 'Ship Date']].dtypes)

# --- Feature Engineering ---
df['Order Year']       = df['Order Date'].dt.year
df['Order Month']      = df['Order Date'].dt.month
df['Order Month-Year'] = df['Order Date'].dt.to_period('M')
df['Profit Margin']    = (df['Profit'] / df['Sales']) * 100

print("\nSample after feature engineering:")
print(df[['Sales', 'Profit', 'Profit Margin', 'Order Year', 'Order Month']].head())

print("\nBasic statistics:")
print(df[['Sales', 'Profit', 'Discount', 'Quantity']].describe())

# =============================================================================
# TASK 2: Data Visualization with Matplotlib
# =============================================================================
print("\n" + "="*60)
print("TASK 2 — Matplotlib Visualizations")
print("="*60)

# ── Interactive Line Chart: Sales Trends Over Years ───────────────────────────
# Yearly sales by category
yearly_sales = df.groupby(['Order Year', 'Category'])['Sales'].sum().reset_index()
yearly_total = df.groupby('Order Year')['Sales'].sum()

fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# Overall yearly sales trend
axes[0].plot(yearly_total.index, yearly_total.values,
             marker='o', linewidth=2.5, markersize=8, color='steelblue', label='Total Sales')

# Annotate each point
for year, val in yearly_total.items():
    axes[0].annotate(f'${val:,.0f}',
                     xy=(year, val), xytext=(0, 12),
                     textcoords='offset points', ha='center', fontsize=9,
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', alpha=0.8))

axes[0].set_title('Annual Sales Trend — US Superstore (All Categories)',
                  fontsize=14, fontweight='bold')
axes[0].set_xlabel('Year', fontsize=12)
axes[0].set_ylabel('Total Sales ($)', fontsize=12)
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# Per category
colors = {'Furniture': '#E74C3C', 'Office Supplies': '#3498DB', 'Technology': '#2ECC71'}
for category, color in colors.items():
    cat_data = yearly_sales[yearly_sales['Category'] == category]
    axes[1].plot(cat_data['Order Year'], cat_data['Sales'],
                 marker='s', linewidth=2, markersize=7, label=category, color=color)

axes[1].set_title('Annual Sales Trend by Category', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Year', fontsize=12)
axes[1].set_ylabel('Sales ($)', fontsize=12)
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
axes[1].grid(True, alpha=0.3)
axes[1].legend(title='Category')

plt.tight_layout()
plt.savefig('sales_trend_matplotlib.png', dpi=150)
plt.show()
print("Plot saved: sales_trend_matplotlib.png")

# ── Sales Distribution by State (Map-style bar chart) ─────────────────────────
# Since we only have US data, build a sales heatmap by region and state
state_sales  = df.groupby('State')['Sales'].sum().sort_values(ascending=False)
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Top 20 states
top_20 = state_sales.head(20)
bars = axes[0].bar(range(len(top_20)), top_20.values,
                   color=plt.cm.Blues(np.linspace(0.4, 0.9, len(top_20))))
axes[0].set_xticks(range(len(top_20)))
axes[0].set_xticklabels(top_20.index, rotation=45, ha='right', fontsize=9)
axes[0].set_title('Top 20 States by Sales', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Sales ($)')
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
axes[0].grid(axis='y', alpha=0.3)

# Region breakdown
region_colors = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12']
wedges, texts, autotexts = axes[1].pie(
    region_sales.values,
    labels=region_sales.index,
    autopct='%1.1f%%',
    colors=region_colors,
    startangle=90,
    pctdistance=0.85
)
for text in autotexts:
    text.set_fontsize(11)
    text.set_fontweight('bold')
axes[1].set_title('Sales Distribution by Region', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('sales_by_state_matplotlib.png', dpi=150)
plt.show()
print("Plot saved: sales_by_state_matplotlib.png")

print("\nGeographic Insights:")
print(f"  Top state: {state_sales.index[0]} (${state_sales.iloc[0]:,.0f})")
print(f"  Top region: {region_sales.index[0]} (${region_sales.iloc[0]:,.0f})")
print(f"  Top 5 states = {(state_sales.head(5).sum()/df['Sales'].sum())*100:.1f}% of total sales")

# =============================================================================
# TASK 3: Data Visualization with Seaborn
# =============================================================================
print("\n" + "="*60)
print("TASK 3 — Seaborn Visualizations")
print("="*60)

# ── Bar Chart: Top 10 Products by Sales ───────────────────────────────────────
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 8))
ax = sns.barplot(x=top_products.values, y=top_products.index,
                 palette='Blues_r', orient='h')

plt.title('Top 10 Products by Sales\nSeaborn — Executive Summary',
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Total Sales ($)', fontsize=12, fontweight='bold')
plt.ylabel('Product Name', fontsize=12, fontweight='bold')

for i, (product, sales) in enumerate(top_products.items()):
    ax.text(sales + max(top_products.values) * 0.01, i,
            f'${sales:,.0f}', va='center', fontsize=9, fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('top_products_seaborn.png', dpi=150)
plt.show()
print("Plot saved: top_products_seaborn.png")

print("\nTop 10 Products Insights:")
print(f"  #1 product: {top_products.index[0]}")
print(f"  #1 sales: ${top_products.iloc[0]:,.0f}")
print(f"  Top 10 products = {(top_products.sum()/df['Sales'].sum())*100:.1f}% of total sales")

# ── Scatter Plot: Profit vs Discount ─────────────────────────────────────────
plt.figure(figsize=(12, 7))

sns.scatterplot(data=df, x='Discount', y='Profit',
                hue='Category', alpha=0.5, s=40,
                palette={'Furniture': '#E74C3C', 'Office Supplies': '#3498DB', 'Technology': '#2ECC71'})

# Regression line for each category
for category, color in [('Furniture', '#E74C3C'), ('Office Supplies', '#3498DB'), ('Technology', '#2ECC71')]:
    cat_data = df[df['Category'] == category]
    sns.regplot(data=cat_data, x='Discount', y='Profit',
                scatter=False, color=color,
                line_kws={'linewidth': 1.5, 'linestyle': '--'}, label=f'{category} trend')

plt.axhline(y=0, color='black', linestyle='-', alpha=0.4, linewidth=1.5)
plt.text(0.52, 80, 'Break-even line', fontsize=10, alpha=0.6)

plt.title('Profit vs Discount Analysis by Category\nSeaborn — Discount Strategy Insights',
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Discount Rate', fontsize=12, fontweight='bold')
plt.ylabel('Profit ($)', fontsize=12, fontweight='bold')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('profit_vs_discount_seaborn.png', dpi=150)
plt.show()
print("Plot saved: profit_vs_discount_seaborn.png")

print("\nDiscount Insights:")
for cat in df['Category'].unique():
    cat_data = df[df['Category'] == cat]
    loss_rate = (cat_data[cat_data['Discount'] > 0.2]['Profit'] < 0).mean() * 100
    print(f"  {cat}: {loss_rate:.1f}% of >20% discounts result in losses")

# =============================================================================
# TASK 4: Comparative Analysis
# =============================================================================
print("\n" + "="*60)
print("TASK 4 — Comparative Analysis: Matplotlib vs Seaborn")
print("="*60)

print("""
MATPLOTLIB vs SEABORN — Comparative Analysis
=============================================

MATPLOTLIB
----------
Strengths:
  • Full control over every visual element (axes, ticks, annotations)
  • Better for custom interactive charts and animations
  • Direct integration with ipywidgets for dynamic filtering
  • Flexible subplot layouts (plt.subplots)

Weaknesses:
  • More verbose code for styled charts
  • Default aesthetics are basic and need manual styling
  • Statistical overlays (regression lines) require manual implementation

Best for: Time-series, custom dashboards, annotated charts

SEABORN
-------
Strengths:
  • Beautiful default aesthetics and color palettes
  • Built-in statistical functions (regplot, heatmap, boxplot)
  • Concise syntax — fewer lines for polished results
  • Excellent for categorical and distribution plots

Weaknesses:
  • Less flexible for non-standard layouts
  • Harder to add custom interactivity
  • Some chart types not available

Best for: EDA, executive presentations, statistical visualizations

RECOMMENDATION:
  → Use Matplotlib for exploration, control, and interactivity.
  → Use Seaborn for presentation-ready, statistically-rich visuals.
  → In practice: combine both — Seaborn on top of Matplotlib.
""")

# =============================================================================
# TASK 5: Summary Dashboard + Key Insights
# =============================================================================
print("\n" + "="*60)
print("TASK 5 — Summary Dashboard & Key Insights")
print("="*60)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('US Superstore — Interactive Data Visualization Dashboard',
             fontsize=16, fontweight='bold', y=1.01)

# 1. Yearly sales trend
ax1.plot(yearly_total.index, yearly_total.values,
         marker='o', linewidth=2.5, color='steelblue', markersize=8)
ax1.set_title('Annual Sales Trend', fontweight='bold')
ax1.set_xlabel('Year')
ax1.set_ylabel('Sales ($)')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax1.grid(True, alpha=0.3)
for year, val in yearly_total.items():
    ax1.annotate(f'${val/1e6:.1f}M', xy=(year, val), xytext=(0, 8),
                 textcoords='offset points', ha='center', fontsize=8)

# 2. Sales by category (Seaborn)
cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
sns.barplot(data=cat_sales, x='Category', y='Sales', ax=ax2,
            palette=['#E74C3C', '#3498DB', '#2ECC71'])
ax2.set_title('Sales by Category', fontweight='bold')
ax2.set_ylabel('Sales ($)')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax2.grid(axis='y', alpha=0.3)

# 3. Top 10 states
top_10 = state_sales.head(10)
ax3.barh(range(len(top_10)), top_10.values,
         color=plt.cm.Blues(np.linspace(0.5, 0.9, len(top_10))))
ax3.set_yticks(range(len(top_10)))
ax3.set_yticklabels(top_10.index, fontsize=9)
ax3.set_title('Top 10 States by Sales', fontweight='bold')
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax3.grid(axis='x', alpha=0.3)

# 4. Profit vs Discount
for cat, color in [('Furniture', '#E74C3C'), ('Office Supplies', '#3498DB'), ('Technology', '#2ECC71')]:
    cat_data = df[df['Category'] == cat]
    ax4.scatter(cat_data['Discount'], cat_data['Profit'],
                label=cat, alpha=0.4, s=15, color=color)
ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5)
ax4.set_title('Profit vs Discount by Category', fontweight='bold')
ax4.set_xlabel('Discount')
ax4.set_ylabel('Profit ($)')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('superstore_dashboard_interactive.png', dpi=150)
plt.show()
print("Dashboard saved: superstore_dashboard_interactive.png")

# Final Key Insights
total_sales  = df['Sales'].sum()
total_profit = df['Profit'].sum()
margin       = total_profit / total_sales * 100

print("\n=== KEY INSIGHTS ===\n")
print(f"1. REVENUE & PROFIT")
print(f"   Total Revenue: ${total_sales:,.0f} | Profit: ${total_profit:,.0f} | Margin: {margin:.1f}%")
print(f"\n2. SALES TREND")
print(f"   Sales grew from ${yearly_total.min():,.0f} to ${yearly_total.max():,.0f}")
print(f"   Growth: {((yearly_total.max()-yearly_total.min())/yearly_total.min())*100:.0f}% over the period")
print(f"\n3. TOP GEOGRAPHY")
print(f"   California leads with ${state_sales.iloc[0]:,.0f} in sales")
print(f"   Top 5 states = {(state_sales.head(5).sum()/total_sales)*100:.1f}% of total revenue")
print(f"\n4. DISCOUNT WARNING")
high_disc = df[df['Discount'] > 0.2]
print(f"   {(high_disc['Profit'] < 0).mean()*100:.1f}% of discounts >20% result in losses")
print(f"   Recommendation: cap discounts at 20%")
print(f"\n5. TOP PRODUCT")
print(f"   {top_products.index[0]}")
print(f"   Generates ${top_products.iloc[0]:,.0f} in sales")
