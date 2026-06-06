import random


# ============================================================
# 🌟 Exercise 1: Pets
# ============================================================

class Pets:
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())


class Cat:
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'


class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'


class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'


# Step 1: Siamese class
class Siamese(Cat):
    def sing(self, sounds):
        return f'{sounds}'


# Step 2: List of cat instances
bengal_obj    = Bengal("Simba", 3)
chartreux_obj = Chartreux("Luna", 5)
siamese_obj   = Siamese("Nala", 2)

all_cats = [bengal_obj, chartreux_obj, siamese_obj]

# Step 3: Create Pets instance
sara_pets = Pets(all_cats)

# Step 4: Walk
print("=== Exercise 1: Pets ===")
sara_pets.walk()


# ============================================================
# 🌟 Exercise 2: Dogs
# ============================================================

class Dog:
    def __init__(self, name, age, weight):
        self.name   = name
        self.age    = age
        self.weight = weight

    def bark(self):
        return f"{self.name} is barking"

    def run_speed(self):
        return self.weight / self.age * 10

    def fight(self, other_dog):
        my_power    = self.run_speed() * self.weight
        other_power = other_dog.run_speed() * other_dog.weight
        if my_power > other_power:
            return f"{self.name} won the fight!"
        elif other_power > my_power:
            return f"{other_dog.name} won the fight!"
        else:
            return "It's a tie!"


# Step 2: Dog instances
dog1 = Dog("Rex",   3, 30)
dog2 = Dog("Bella", 5, 20)
dog3 = Dog("Max",   2, 25)

# Step 3: Test methods
print("\n=== Exercise 2: Dogs ===")
print(dog1.bark())
print(f"{dog2.name}'s run speed: {dog2.run_speed():.2f}")
print(dog1.fight(dog2))
print(dog2.fight(dog3))


# ============================================================
# 🌟 Exercise 3: Dogs Domesticated
# ============================================================

class PetDog(Dog):
    def __init__(self, name, age, weight):
        super().__init__(name, age, weight)
        self.trained = False

    def train(self):
        print(self.bark())
        self.trained = True

    def play(self, *args):
        all_names = [self.name] + [dog.name for dog in args]
        print(f"{', '.join(all_names)} all play together")

    def do_a_trick(self):
        if self.trained:
            tricks = [
                "does a barrel roll",
                "stands on his back legs",
                "shakes your hand",
                "plays dead"
            ]
            print(f"{self.name} {random.choice(tricks)}")
        else:
            print(f"{self.name} is not trained yet!")


# Step 3: Test PetDog
print("\n=== Exercise 3: Dogs Domesticated ===")
fido  = PetDog("Fido",  2, 10)
buddy = PetDog("Buddy", 4, 15)
max_  = PetDog("Max",   3, 12)

fido.train()
fido.play(buddy, max_)
fido.do_a_trick()

buddy.do_a_trick()   # not trained yet
buddy.train()
buddy.do_a_trick()


# ============================================================
# 🌟 Exercise 4: Family and Person Classes
# ============================================================

class Person:
    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age        = age
        self.last_name  = ""

    def is_18(self):
        return self.age >= 18


class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members   = []

    def born(self, first_name, age):
        person           = Person(first_name, age)
        person.last_name = self.last_name
        self.members.append(person)

    def check_majority(self, first_name):
        for person in self.members:
            if person.first_name == first_name:
                if person.is_18():
                    print("You are over 18, your parents Jane and John accept "
                          "that you will go out with your friends")
                else:
                    print("Sorry, you are not allowed to go out with your friends.")
                return
        print(f"{first_name} is not a member of the family.")

    def family_presentation(self):
        print(f"\nFamily: {self.last_name}")
        for person in self.members:
            print(f"  - {person.first_name}, age {person.age}")


# Test
print("\n=== Exercise 4: Family and Person ===")
my_family = Family("Smith")

my_family.born("Jane",  45)
my_family.born("John",  47)
my_family.born("Alice", 20)
my_family.born("Tom",   15)

my_family.family_presentation()
my_family.check_majority("Alice")
my_family.check_majority("Tom")
