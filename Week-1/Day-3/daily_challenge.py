# Challenge 1

word = input("Enter a word: ")
result = {}

for index, letter in enumerate(word):
    if letter in result:
        result[letter].append(index)
    else:
        result[letter] = [index]

print(result)

# Challenge 2

items_purchase = {"Water": "$1", "Bread": "$3", "TV": "$1,000", "Fertilizer": "$20"}
wallet = "$300"

wallet = int(wallet.replace("$", "").replace(",", ""))
basket = []
for item,price in items_purchase.items():
    price = int(price.replace("$","").replace(",",""))
    if price < wallet:
        basket.append(item)
        wallet = wallet - price 

if basket == [""]:
    print("nothing")


print(basket)