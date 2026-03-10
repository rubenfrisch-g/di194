# Exercice 1:

# What is data analysis?
# Data analysis is the process of examining, cleaning, and interpreting data to find patterns, draw conclusions, and support decision-making.

# Why is data analysis important in modern contexts?
# It is important because everyone but also organizations generate large amounts of data and use analysis to make better decisions, improve efficiency, and predict future trends.

# Three areas where data analysis is applied today:
# Healthcare: analyzing patient data to improve treatments and track diseases
# Sport: to follow to physical fitenss of the player and to prevent injuries
# Marketing: studying customer behavior to improve products and advertising

# Exercie 2:

import pandas as pd

sleep = pd.read_csv("Spend_Sleeping.csv")
mental = pd.read_csv("Mental_health_Depression_disorder_Data.csv")
credit = pd.read_csv("clean_dataset.csv")

print(sleep.head())
print(mental.head())
print(credit.head())

# Exercice 3

def identify_types(df):
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            print(column, "- Quantitative (numerical values)")
        else:
            print(column, "- Qualitative (categories or text)")

print("Sleep Dataset:")
identify_types(sleep)

print("\nMental Health Dataset:")
identify_types(mental)

print("\nCredit Card Dataset:")
identify_types(credit)


# Exercice 4

# The Iris dataset contains both quantitative and qualitative variables.
# The sepal and petal measurements are quantitative because they represent numerical measurements of flower characteristics. 
# The species column is qualitative because it represents categories of flowers rather than numerical values.

# Exercice 5

# load the dataset
sleep_data = pd.read_csv("sleep_data.csv")

# display the first rows
print(sleep_data.head())

# display column names
print("\nColumns in the dataset:")
print(sleep_data.columns)

# Exercice 6
# A company’s financial reports stored in an Excel file – Structured data
# The data is organized in rows and columns with a clear format, making it easy to analyze.

# Photographs uploaded to a social media platform – Unstructured data
# Images do not follow a predefined structure like tables or databases.

# A collection of news articles on a website – Unstructured data
# Articles consist mostly of free text, which does not follow a fixed data structure.

# Inventory data in a relational database – Structured data
# The data is organized into tables with defined fields and relationships.

# Recorded interviews from a market research study – Unstructured data
# Audio recordings do not have a predefined structure and require processing to analyze. 

# Exercice 7

# Blog posts about travel experiences – Use text analysis to extract information such as destination, dates, and activities, and store it in a table.

# Audio recordings of customer service calls – Use speech-to-text transcription, then extract key fields like issue type, call duration, and resolution.

# Handwritten notes from a brainstorming session – Use OCR (Optical Character Recognition) to convert handwriting into text, then organize ideas into categories.

# Video tutorial on cooking – Transcribe the video and extract structured information such as recipe name, ingredients, and steps.

# Exercice 8

train_data = pd.read_csv("train.csv")
print(train_data.head())

# Exercice 9

data = {
    "Name": ["Sixtine", "Ruben", "Yael"],
    "Age": [17, 18, 16],
    "City": ["Tel-Aviv", "Jerusalem", "Brussels"]
}

df = pd.DataFrame(data)

df.to_excel("data.xlsx", index=False)

df.to_json("data.json", orient="records")

print(df)

# Exercice 10

url = "https://jsonplaceholder.typicode.com/posts"
data = pd.read_json(url)
print(data.head())






