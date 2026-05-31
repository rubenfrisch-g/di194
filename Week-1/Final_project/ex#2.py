import random

wordslist = ['correction', 'childish', 'beach', 'python', 'assertive', 'interference', 'complete', 'share', 'credit card', 'rush', 'south']
word = random.choice(wordslist)

### YOUR CODE STARTS FROM HERE ###

HANGMAN_STAGES = [
    """
       -----
       |   |
           |
           |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
           |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ========="""
]

def display_word(word, guessed_letters):
    display = ""
    for char in word:
        if char == " ":
            display += "  "
        elif char in guessed_letters:
            display += char + " "
        else:
            display += "* "
    return display.strip()

def play_hangman():
    guessed_letters = set()
    wrong_guesses   = 0
    max_wrong       = 6

    print("\n🎮 Welcome to Hangman!")
    print(f"The word has {len(word.replace(' ', ''))} letters", end="")
    if " " in word:
        print(" (it's a phrase!)", end="")
    print("\n")

    while wrong_guesses < max_wrong:
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"\nWord: {display_word(word, guessed_letters)}")
        print(f"Wrong guesses left: {max_wrong - wrong_guesses}")
        if guessed_letters:
            print(f"Letters guessed: {', '.join(sorted(guessed_letters))}")

        # Check win
        if all(c in guessed_letters or c == " " for c in word):
            print(f"\n🎉 You won! The word was: '{word}'")
            return

        # Get input
        guess = input("\nGuess a letter: ").lower().strip()

        if len(guess) != 1 or not guess.isalpha():
            print("❌ Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print(f"⚠️  You already guessed '{guess}'. Try another letter.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            count = word.count(guess)
            print(f"✅ '{guess}' is in the word! ({count} time{'s' if count > 1 else ''})")
        else:
            wrong_guesses += 1
            body_parts = ["head", "body", "left arm", "right arm", "left leg", "right leg"]
            print(f"❌ '{guess}' is not in the word. +1 body part: {body_parts[wrong_guesses - 1]}")

    # Game over
    print(HANGMAN_STAGES[max_wrong])
    print(f"\n💀 Game over! The word was: '{word}'")

play_hangman()