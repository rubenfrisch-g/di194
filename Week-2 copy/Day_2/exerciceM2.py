class Dog:

    def __init__ (self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def bark(self):
        return f"{self.name} is barking"

    def run_speed(self):
        return (self.weight / self.age) * 10
    
    def fight(self, other_dog):
        my_power = self.run_speed() * self.weight
        other_power = other_dog.run_speed() * other_dog.weight
        if my_power > other_power:
            print(f"{self.name} wins!")
        elif my_power < other_power:
            print(f"{other_dog.name} wins!")
        else:
            print("It's a draw!")

dog1 = Dog("Rex", 5, 20)
dog2 = Dog("Max", 3, 25)
dog3 = Dog("Bella", 7, 18)

print(dog1.bark())
print(dog2.run_speed())
print(dog1.fight(dog3))