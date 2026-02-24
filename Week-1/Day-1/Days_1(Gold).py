# Exercie 1

print("Hello word " * 4 + "I love python " * 4)

# Exercie 2

try:
    number = int(input("Choose a month from 1 to 12: "))

    if number in [3, 4, 5]:
        print("Spring")
    elif number in [6, 7, 8]:
        print("Summer")
    elif number in [9, 10, 11]:
        print("Autumn")
    elif number in [12, 1, 2]:
        print("Winter")
    else:
        print("That is not a valid month.")

except:
    print("That is not a valid number.")



   
