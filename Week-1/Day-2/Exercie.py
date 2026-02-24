# Exercie 1

my_fav_numbers = {2, 4, 6}
print(my_fav_numbers)

my_fav_numbers.add(8)
my_fav_numbers.add(10)
print(my_fav_numbers)

my_fav_numbers.remove(10)
print(my_fav_numbers)

friend_fav_numbers = {8, 9}
print(friend_fav_numbers)

our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)
print(our_fav_numbers)

# Exercice 2

numbers = (1, 2, 3)

numbers.append(4) # Try to add a number will produce an error 

# Exercie 3

basket = ["Banana", "Apples", "Oranges", "Blueberries"]

basket.remove("Banana")
print(basket)

basket.remove("Blueberries")
print(basket)

basket.append("Kiwi")
print(basket)

basket.insert(0, "Apples")
print(basket)

result = basket.count("Apples")
print(result)

basket.clear()
print(basket)

# Exercie 4

# A float is a number that contains a decimal point, like 3.5 or 2.0
# An integer is a whole number without a decimal part, like 3 or -7

FI_numbers = [i / 2 for i in range(3, 11)]
print(FI_numbers)

# Exercie 5

for num in range(1,21):
    print(num)

for index in range(21):
    if index % 2 == 0:
        print(index) 

# Exercie 6

name = input("Hey boss, what is your name? ")

while True:
    if len(name) < 3 or name.isdigit():
        name = input("Give a correct name: ")
        continue

    print("Thank you")
    break

# Exercie 7

fav_fruit = input("Enter your favorite fruits separated by spaces: ")
fav_fruit_list = fav_fruit.split()

other_fruit = input("Give me another fruit")

if other_fruit in fav_fruit_list:
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")
    
# Exercie 8

list_of_toppings = []

while True:
    toppings = input("Enter a topping (type 'quit' to finish): ")

    if toppings == "quit":
        print(f"Adding {list_of_toppings} to your pizza")
        break
    else:
        list_of_toppings.append(toppings)

number_of_toppings = len(list_of_toppings)
pizza_price = number_of_toppings * 2,5 + 10

print(f"The price of your pizza with all the toppings is {pizza_price}$")

# Exercie 9

total_cost = 0

while True:
    age = input("Enter age (or type 'quit' to finish): ")
    
    if age == "quit":
        break
    
    age = int(age)
    
    if age < 3:
        cost = 0
    elif age <= 12:
        cost = 10
    else:
        cost = 15
    
    total_cost += cost

print(f"Total ticket cost: {total_cost}$" )