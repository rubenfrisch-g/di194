# Exercice 1
import numpy as np

arr = np.arange(10)
print(arr)

# Exercice 2
lst = [3.14, 2.17, 0, 1, 2]

arr = np.array(lst).astype(int)
print(arr)

# Exercice 3
arr = np.arange(1, 10).reshape(3, 3)
print(arr)

# Exercice 4
arr = np.random.rand(4, 5)
print(arr)

# Exercice 5
array = np.array([
    [21,22,23,22,22],
    [20,21,22,23,24],
    [21,22,23,22,22]
])

second_row = array[1]
print(second_row)

# Exercice 6
arr = np.arange(10)

reversed_arr = arr[::-1]
print(reversed_arr)
# Exercice 7
identity = np.eye(4)
print(identity)

# Exercice 8
arr = np.arange(10)

print("Sum:", arr.sum())
print("Average:", arr.mean())

# Exercice 9
arr = np.arange(1, 21).reshape(4, 5)
print(arr)

# Exercice 10
arr = np.arange(10)

odd_numbers = arr[arr % 2 != 0]
print(odd_numbers)

