# Exercice 1

# Data vizualization important because it helps people to understand data more easily.
# Graphs and charts allow analysts to see patern and trends, detect anomalies or outliers ans suurize large datasets quickly.

# A line graph is used to show how a variable chage over time.
# It helps identify trends, increases, or decreases in the data.

# Exercice 2

import matplotlib.pyplot as plt

day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
temp = [72, 74, 76, 80, 82, 78, 75]

plt.plot(day, temp)

plt.title('Temperature variation over a Week')
plt.xlabel('Day')
plt.ylabel('Temperature (°F)')
plt.show()

# # Exercice 3

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
sales = [5000, 5500, 6200, 7000, 7500]

plt.bar(months, sales)

plt.title('Monthly sales')
plt.xlabel('Month')
plt.ylabel('Sales Amount ($)')

plt.show()

# Exercice 4

import seaborn as sns 
import pandas as pd

df = pd.read_csv('Week-3/Day-4/Student Mental health.csv')

sns.histplot(data=df, x='What is your CGPA?', color='skyblue')

plt.title('Distribution of students CGPA')
plt.xlabel('CGPA')
plt.show()

# Exercice 5

sns.countplot(data=df, x='Choose your gender', hue='Do you have Anxiety?')

plt.title('Anxiety Levels Across Different Genders')
plt.show()

# Exercice 6

df = pd.read_csv('Week-3/Day-4/Student Mental health.csv')

df["panic_numeric"] = df["Do you have Panic attack?"].map({"Yes": 1, "No": 0})

sns.scatterplot(
    data=df,
    x="Age",
    y="panic_numeric",
    style="panic_numeric",
    hue="panic_numeric"
)

plt.title("Relationship Between Age and Panic Attacks")
plt.xlabel("Age")
plt.ylabel("Panic Attacks (1 = Yes, 0 = No)")

plt.show()

