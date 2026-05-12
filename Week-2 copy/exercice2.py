# Exercise 2 — Dogs

# Step 1: Create the Dog class
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