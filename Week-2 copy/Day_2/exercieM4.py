class Person:
    def __init__(self, first_name, age, last_name):
        self.first_name = first_name
        self.age = age 
        self.last_name = last_name

    def is_18(self):
        if self.age >= 18:
            return True
        else:
            return False
        
class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []

    def born(self, first_name, age):
        new_person = Person(first_name, age)
        new_person.last_name = self.last_name
        self.members.append(new_person)

    def check_majority(self, first_name):
        for member in self.members:
            if member.first_name == first_name:
                if member.is_18():
                    print("You are over 18, your parents Jane and John accept that you will go out with your friends")
                else:
                    print("Sorry, you are not allowed to go out with your friends.")
                return
        print("Person not found in the family.")

    def family_presentation(self):
        print(f"Family name: {self.last_name}")
        for member in self.members:
            print(f"{member.first_name}, {member.age} years old")

        
frisch_family = Family("Frisch")

frisch_family.born("Emmanuel", 54)
frisch_family.born("Muriel", 50)
frisch_family.born("Lauren", 23)
frisch_family.born("Aaron", 22)
frisch_family.born("Ruben", 18)

frisch_family.check_majority("Muriel")
frisch_family.check_majority("Ruben")

frisch_family.family_presentation()