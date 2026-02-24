# Exercice 1

def display_message():
    print("I am learning about functions in Python.")

display_message()

# Exercice 2

def favorite_book(title):
    print(f"One of my favorite books is {title}")

favorite_book("Alice in Wonderland")

# Exercie 3

def describe_city(city, country = "Unknown"):
    print(f"{city} is in {country}")

describe_city("Reykjavik", "iceland")
describe_city("Paris")

# Exercice 4

import random

def number_random(num):
    r_num = random.randint(1,100)
    if num == r_num:
        print("Success!")
    else:
        print(f"Fail! Your num: {num}, Random number: {r_num}")

number_random(12)

# Exercice 5

def make_shirt(size = "large", text = "I love Python"):
    print(f"Your shirt's size is {size} and the text on it is : {text}")

make_shirt("M", "I am working")

# Exercice 6

magician_names = ['Harry Houdini', 'David Blaine', 'Criss Angel']

def show_magicians(names):
    for magician in names:
        print(magician)
    


def make_great(great):
    for magician in great:
        print(f"{magician} the Great")

   
make_great(magician_names)

#  Exercice 7

def get_random_temp():
    return random.uniform(-10,41)

def main():
    temp = get_random_temp()
    print(f"The temperature right now is {temp:.1f} degree Celsius")

    if temp <= 0:
        print("Brrr, that’s freezing! Wear some extra layers today.")
    elif 0 < temp <= 16:
        print("Quite chilly! Don’t forget your coat.")
    elif 16 < temp <= 23:
        print("Nice weather.")
    elif 24 <= temp <= 32:
        print("A bit warm, stay hydrated.")
    else:
        print("It’s really hot! Stay cool.")

main()