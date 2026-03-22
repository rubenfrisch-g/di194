import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

df = pd.read_excel('Week-3/Day-5/US Superstore data.xls')

most_sales = df.groupby('State')['Sales'].sum().sort_values(ascending= False)

top_states = most_sales.head(10).reset_index()

print(most_sales)

sns.barplot(data=top_states, x= "State", y= "Sales")

plt.title('Most sales by states')
plt.xlabel('States')
plt.ylabel('Sales')
plt.xticks(rotation=45)
plt.show()

newY_cal = df[df['State'].isin(['New York', 'California'])]
result = newY_cal.groupby('State')[['Sales', 'Profit']].sum()
print(result)

difference = result.loc['California'] - result.loc['New York']
print(difference)

ny_data = df[df['State'] == 'New York']
customer_sales = ny_data.groupby('Customer Name')[['Sales', 'Profit']].sum()
top_customer = customer_sales.sort_values(by = 'Sales', ascending = False).head(10)
print(top_customer)

sns.barplot(data = top_customer, x='Customer Name', y='Sales')

plt.title("Top customer in new york (sales)")
plt.xticks(rotation = 90)
plt.show()

profit_by_state = df.groupby('State')['Profit'].sum().sort_values(ascending=False)
print(profit_by_state.head(10))
print(profit_by_state.tail(10))

customer_profit = df.groupby("Customer Name")["Profit"].sum().sort_values(ascending=False)
cumulative_profit = customer_profit.cumsum()
total_profit = customer_profit.sum()
cumulative_percentage = cumulative_profit / total_profit
total_customers = len(customer_profit)
customers_80 = cumulative_percentage[cumulative_percentage <= 0.8]

pareto_ratio = len(customers_80) / total_customers

print(f"{pareto_ratio:.2%} of customers generate 80% of profit")

top_sale = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(20).reset_index()
top_profit = df.groupby('State')['Profit'].sum().sort_values(ascending=False).head(20).reset_index()
print(top_profit)
print(top_sale)

sns.barplot(data=top_sale, x="Sales", y="State")
plt.title("Top 20 Cities by Sales")
plt.show()

sns.barplot(data=top_profit, x="Profit", y="State")
plt.title("Top 20 Cities by Profit")
plt.show()


top_customers = df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(20).reset_index()
print(top_customers)

sns.barplot(data=top_customers, x='Customer Name', y='Sales')
plt.title('Top 20 customers by sales')
plt.xticks(rotation=90)
plt.show()

customer_sales = df.groupby("Customer Name")["Sales"].sum()

customer_sales = customer_sales.sort_values(ascending=False)

cumulative_sales = customer_sales.cumsum()

total_sales = customer_sales.sum()
cumulative_percentage = cumulative_sales / total_sales

plt.plot(cumulative_percentage.values)

plt.axhline(0.8)  
plt.title("Pareto Curve - Sales by Customers")
plt.xlabel("Customers (sorted)")
plt.ylabel("Cumulative Sales %")
plt.show()

# Marketing should focus on high-sales and high-profit states such as California and New York. 
# Cities with high sales but low profit require margin optimization, while highly profitable cities should be targeted for expansion. 
# Low-performing areas should not be prioritized until profitability improves.