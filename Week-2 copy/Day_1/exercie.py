class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age  = cat_age

# Step 1: Create three cat objects
cat1 = Cat("fluffy", 7)
cat2 = Cat("Figaro", 14)
cat3 = Cat("hatoul", 2)

# Step 2: Write a function to find the oldest cat
def find_oldest_cat(cat1, cat2, cat3):
    if cat1.age > cat2.age:
        return cat1
    elif cat2.age > cat3.age:
        return cat2
    else:
        return cat3
    
oldest = find_oldest_cat(cat1, cat2, cat3)
print(f"The oldest cat is {oldest.name}, and is {oldest.age} years old.")


# Exercice 2

class Dog:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def bark(self):
        print(f"{self.name} goes woof!")

    def jump(self):
        print(f"{self.name} jumps {self.height * 2} cm hight")


davids_dog = Dog("Rex", 50)
sarahs_dog = Dog("Bella", 35)

# Step 3: Print details and call methods

print(f"{davids_dog.name} is {davids_dog.height} cm tall.")
davids_dog.bark()
davids_dog.jump()

print()

print(f"{sarahs_dog.name} is {sarahs_dog.height} cm tall.")
sarahs_dog.bark()
sarahs_dog.jump()

# Step 4: Compare sizes

if davids_dog.height > sarahs_dog.height:
    print(f"{davids_dog.name} is taller.")
elif sarahs_dog.height > davids_dog.height:
    print(f"{sarahs_dog.name} is taller.")
else:
    print("Both dogs are the same height.")


# Exercice 3

class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics 

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)

happy_birthday = Song([
    "Happy birthday to you",
    "Happy birthday to you",
    "Happy birthday dear friend",
    "Happy birthday to you"
])

happy_birthday.sing_me_a_song()

# Exercice 4

class Zoo:
    def __init__(self, zoo_name):
        self.name = zoo_name
        self.animals = []

    def add_animal(self, new_animal):
        if new_animal not in self.animals:
            self.animals.append(new_animal)

    def get_animals(self):
        print(self.animals)
        
    def sell_animals(self, animal_sold):
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)
    
    def sort_animals(self):
        self.groups = {}
        for animal in sorted(self.animals):
            letter = animal[0]
            if letter not in self.groups:
                self.groups[letter] = []
        self.groups[letter].append(animal)

    def get_groups(self):
        print(self.groups)


brooklyn_safari = Zoo("Brooklyn Safari")

brooklyn_safari.add_animal("Giraffe")
brooklyn_safari.add_animal("Bear")
brooklyn_safari.add_animal("Baboon")
brooklyn_safari.get_animals()
brooklyn_safari.sell_animals("Bear")
brooklyn_safari.get_animals()
brooklyn_safari.sort_animals()
brooklyn_safari.get_groups()