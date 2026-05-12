class Pets:

    is_lazy = False

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def description(self):
        print(f"{self.name} is {self.age} years old.")

    def make_sound(self):
        print("...")

class Cat(Pets):

    is_lazy = True

    def __init__(self, name: str, age: int, indoor: bool):
        super().__init__(name, age)
        self.indoor = indoor
    
    def make_sound(self):
        print(f"{self.name} says: Meow!")


class Dog(Pets):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def make_sound(self):
        print(f"{self.name} says: Woof!")

    def fetch(self, item: str):
        print(f"{self.name} fetches the {item}!")