first = "Hello World"
#This is a comment.
print("I AM A COMPUTER!")
if 1 < 2 and 4 > 2 :
    print("Math is Fun")
nope = None
True and False
print(len("What's my length?"))
print("i am shouting".upper())
print(int("1000"))
print("4"+"real")
print(3 * "cool")
print(1 / 0)
type([])
name = input("What is your name ?")
number = int(input("Chose a random number"))
if number < 0 :
    print("That number is less than 0!")
if number > 0 :
    print("That number is greater than 0!")
if number == 0 :
    print("You picked 0!")
print("apple".find("l"))
if int(("xylophne".find("y"))) > 0 :
    print("YEAHHHH y is in the word ")
print("my_string".islower())


# Exercice 2 

def calculate_years(human_Years):
    if human_Years == int(1):
        cat_Years = int(15) 
        dog_Years = int(15)
       
    elif human_Years == int(2):
        cat_Years = int(24)
        dog_Years = int(24)
        
    else:
        cat_Years = 24 + (human_Years - 2) * 4
        dog_Years = 24 + (human_Years - 2) * 5
        

    return [human_Years, cat_Years, dog_Years]

print(calculate_years(int(10)))
print(calculate_years(int(1)))
print(calculate_years(int(2)))