# ============================================================
# 🌟 Exercise 1 : Cats
# ============================================================

class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age


# Step 1: Create cat objects
cat1 = Cat("Whiskers", 3)
cat2 = Cat("Luna", 7)
cat3 = Cat("Mochi", 5)


# Step 2: Function to find the oldest cat
def find_oldest_cat(cat1, cat2, cat3):
    oldest = cat1
    if cat2.age > oldest.age:
        oldest = cat2
    if cat3.age > oldest.age:
        oldest = cat3
    return oldest


# Step 3: Print the oldest cat's details
oldest_cat = find_oldest_cat(cat1, cat2, cat3)
print(f"The oldest cat is {oldest_cat.name}, and is {oldest_cat.age} years old.")


# ============================================================
# 🌟 Exercise 2 : Dogs
# ============================================================

class Dog:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def bark(self):
        print(f"{self.name} goes woof!")

    def jump(self):
        print(f"{self.name} jumps {self.height * 2} cm high!")


# Step 2: Create dog objects
davids_dog = Dog("Rex", 50)
sarahs_dog = Dog("Bella", 35)

# Step 3: Print details and call methods
print(f"\nDavid's dog: {davids_dog.name}, height: {davids_dog.height} cm")
davids_dog.bark()
davids_dog.jump()

print(f"\nSarah's dog: {sarahs_dog.name}, height: {sarahs_dog.height} cm")
sarahs_dog.bark()
sarahs_dog.jump()

# Step 4: Compare dog sizes
print()
if davids_dog.height > sarahs_dog.height:
    print(f"{davids_dog.name} is bigger than {sarahs_dog.name}.")
elif sarahs_dog.height > davids_dog.height:
    print(f"{sarahs_dog.name} is bigger than {davids_dog.name}.")
else:
    print(f"{davids_dog.name} and {sarahs_dog.name} are the same size.")


# ============================================================
# 🌟 Exercise 3 : Who's the song producer?
# ============================================================

class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)


stairway = Song([
    "There's a lady who's sure",
    "all that glitters is gold",
    "and she's buying a stairway to heaven"
])

print()
stairway.sing_me_a_song()


# ============================================================
# 🌟 Exercise 4 : Afternoon at the Zoo
# ============================================================

class Zoo:
    def __init__(self, zoo_name):
        self.name = zoo_name
        self.animals = []

    def add_animal(self, *args):
        for new_animal in args:
            if new_animal not in self.animals:
                self.animals.append(new_animal)
            else:
                print(f"{new_animal} is already in the zoo.")

    def get_animals(self):
        print(f"\nAnimals in {self.name}: {self.animals}")

    def sell_animal(self, animal_sold):
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)
            print(f"{animal_sold} has been sold.")
        else:
            print(f"{animal_sold} is not in the zoo.")

    def sort_animals(self):
        self.animals.sort()
        groups = {}
        for animal in self.animals:
            first_letter = animal[0].upper()
            if first_letter not in groups:
                groups[first_letter] = []
            groups[first_letter].append(animal)
        return groups

    def get_groups(self):
        groups = self.sort_animals()
        print()
        for letter, animals in groups.items():
            print(f"{letter}: {animals}")


# Step 2: Create a Zoo instance
brooklyn_safari = Zoo("Brooklyn Safari")

# Step 3: Use the Zoo methods
brooklyn_safari.add_animal("Giraffe", "Bear", "Baboon", "Lion", "Zebra", "Cat", "Cougar")
brooklyn_safari.get_animals()
brooklyn_safari.sell_animal("Bear")
brooklyn_safari.get_animals()
brooklyn_safari.get_groups()
