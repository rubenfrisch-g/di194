import random


def get_words_from_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        words = content.split()
        return words


def get_random_sentence(length):
    words = get_words_from_file("words.txt")
    random_words = []

    for _ in range(length):
        random_words.append(random.choice(words))

    sentence = " ".join(random_words)
    return sentence


def main():
    try:
        user_input = int(input("Enter sentence length (2-20): "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return

    if user_input < 2 or user_input > 20:
        print("Please enter a number between 2 and 20.")
        return

    sentence = get_random_sentence(user_input)
    print(f"Generated sentence: {sentence}")


main()