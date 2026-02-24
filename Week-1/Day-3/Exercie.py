# Exercice 1

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

result = dict(zip(keys, values))

print(result)

# Exercie 2

family = {}
total_price = 0

while True:
    name = input("Enter a family member's name (or type 'quit'): ")
    
    if name == "quit":
        break
    
    age = int(input(f"Enter {name}'s age: "))
    family[name] = age

price_list = {}

for x,y in family.items():
    if y < 3:
       price = 0
    elif 3 <= y <= 12:
        price = 10
    else:
        price = 15 

    price_list[x] = price
    total_price += price

print(price_list)
print(total_price)

# Exercie 3

brand = {
"name": "Zara",
"creation_date": "1975",
"creator_name": "Amancio Ortega Gaona",
"type_of_clothes": ["men", "women", "children", "home"],
"international_competitors": ["Gap", "H&M", "Benetton"],
"number_stores": 7000,
"major_color": {
    "France": "blue", 
    "Spain": "red", 
    "US": ["pink", "green"]
}}

brand.update({"number_stores": 2,})
print(f"Zara creates cloth for {",".join(brand ["type_of_clothes"])}")
brand.update({"country_creation": "Spain"})
for key in brand.keys():
    if "international_competitors" in brand.keys():
        brand.update({"international_competitors": ["Gap", "H&M", "Benetton", "Desigual"]})

del brand["creation_date"]
print(brand["international_competitors"][-1])
print(brand["major_color"]["US"])
print(len(brand))
print(brand.keys())

# Exercice 4

users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]

dict1 = {}

for i, name in enumerate(users):
    dict1[name] = i

print(dict1)

dict2 = {}

for i, name in enumerate(users):
    dict2[i] = name

print(dict2)

sorted_users = sorted(users)
dict3 = {}

for i, name in enumerate(sorted_users):
    dict3[name] = i

print(dict3)

