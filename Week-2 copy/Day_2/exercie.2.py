class Dog:
    def __init__(self, name: str, age: int, weight: float, breed: str):
        self.name = name
        self.age = age
        self.weight = weight
        self.breed = breed

    def run_speed(self):
        return (self.weight/self.age) * 10
    
    def fight(self, other_dog):
        if self.run_speed > other_dog.run_speed:
            print(f"{self.name} wins!")
        elif self.run_speed < other_dog.run_speed:
            print(f"{other_dog} wins!")
        else:
            print("It's a draw")
    
class Dogs:
    def __init__(self):
        self.pack = []
    
    def add_dog(self, dog):
        self.pack.append(dog)
    
    def fight_all(self):
        for i in range(len(self.pack)):
            for j in range(i + 1, len(self.pack)):
                self.pack[i].fight(self.pack[j])


