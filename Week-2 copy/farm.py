# ============================================================
# 🌟 Old MacDonald's Farm
# ============================================================

class Farm:
    def __init__(self, farm_name):
        self.name = farm_name
        self.animals = {}

    def add_animal(self, animal_type=None, count=1, **kwargs):
        # Support classic call: add_animal('cow', 5)
        if animal_type is not None:
            if animal_type in self.animals:
                self.animals[animal_type] += count
            else:
                self.animals[animal_type] = count

        # Step 8 bonus: support add_animal(cow=5, sheep=2)
        for animal, qty in kwargs.items():
            if animal in self.animals:
                self.animals[animal] += qty
            else:
                self.animals[animal] = qty

    def get_info(self):
        info = f"{self.name}'s farm\n\n"
        for animal, count in self.animals.items():
            info += f"{animal} : {count}\n"
        info += "\n    E-I-E-I-0!"
        return info

    # ── Bonus ──────────────────────────────────────────────

    def get_animal_types(self):
        return sorted(self.animals.keys())

    def get_short_info(self):
        animal_types = self.get_animal_types()
        # Add 's' if count > 1
        animal_names = [
            f"{a}s" if self.animals[a] > 1 else a
            for a in animal_types
        ]
        if len(animal_names) == 1:
            animals_str = animal_names[0]
        else:
            animals_str = ", ".join(animal_names[:-1]) + " and " + animal_names[-1]
        return f"{self.name}'s farm has {animals_str}."


# ── Tests ───────────────────────────────────────────────────

macdonald = Farm("McDonald")

# Classic usage
macdonald.add_animal('cow', 5)
macdonald.add_animal('sheep')
macdonald.add_animal('sheep')
macdonald.add_animal('goat', 12)

print(macdonald.get_info())
# McDonald's farm
#
# cow : 5
# sheep : 2
# goat : 12
#
#     E-I-E-I-0!

print()
print(macdonald.get_short_info())
# McDonald's farm has cows, goats and sheeps.

print()

# Step 8 bonus: kwargs usage
macdonald2 = Farm("McDonald")
macdonald2.add_animal(cow=5, sheep=2, goat=12)
print(macdonald2.get_info())
