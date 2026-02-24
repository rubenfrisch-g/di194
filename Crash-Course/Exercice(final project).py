import random
def number_guessing_game():
    random_number = random.randint(1, 100)
    max_attempts = 7

    print ("Welcome to the number guessing game")
    print ("I'm thinking of a number between 1 and 100, try and guess it!")
    print (f"be careful, you only have {max_attempts} attempts")

    for guess in range(1, max_attempts + 1):
        number = input(f"Attempt {guess}, enter your guess:")
        real_number = int(number)

        if real_number < random_number:
            print("Too low!")
        elif real_number > random_number:
            print("Too high!")
        else:    
            print (f"Congratulations! You guessed it right, the number is {random_number}!")
            break

    else:
        print("You're all out of attempts")
        print(f"The number was {random_number}")
     
number_guessing_game()