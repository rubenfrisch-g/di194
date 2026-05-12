import random
import string

all_letter = string.ascii_lowercase

random_string = ""
for _ in range(5):
    random_string += random.choice(all_letter)

print(random_string)

    