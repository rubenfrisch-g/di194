import random

list_of_numbers = [random.randint(0, 10000) for _ in range(20000)]
target_number   = 3728

# Trouver toutes les paires qui somment au target
seen   = {}
pairs  = []

for num in list_of_numbers:
    complement = target_number - num
    if complement in seen:
        pair = (min(num, complement), max(num, complement))
        if pair not in pairs:
            pairs.append(pair)
    seen[num] = True

# Afficher les résultats
print(f"Pairs that sum to {target_number}:\n")
for a, b in pairs:
    print(f"  {a} and {b} sums to {target_number}")

print(f"\nTotal unique pairs found: {len(pairs)}")
