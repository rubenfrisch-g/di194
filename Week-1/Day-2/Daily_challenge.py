# Challenge 1

list_num = []
number = int(input("Give me one number : "))
lenght = int(input("Give me another number"))

for num in range(1,lenght + 1):
    table = (number * num)
    list_num.append(table)

print(list_num)

# Challenge 2

word = input("Give me a string : ")

result = ""

for w in word:
    if result == "" or w != result[-1]:
        result += w

print(result)
    