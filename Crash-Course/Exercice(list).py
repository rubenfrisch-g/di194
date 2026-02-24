number = [1,2,3,4]
print([1,2,3,4])
print ([n * 20 for n in number])
names = ['Elie', 'Tim', 'Matt']
print([name[0] for name in names])
list = [1,2,3,4,5,6]
even = [lis for lis in list if lis % 2 == 0]
print(even)
list1_ex5 = [1,2,3,4]
list2_ex5 = [3,4,5,6]
print([li for li in list1_ex5 if li in list2_ex5])
lowercase_names = [name.lower() for name in names]
print([low[::-1] for low in lowercase_names])
print([let for let in 'first' if let in 'third'])
print([num for num in range(1,101) if num % 12 == 0])
vowels = ['a','e','i','o','u','y']
print([con for con in 'amazing' if con not in vowels])
list_ex10 = [0,1,2]
print([list_ex10]*3)
full_list = [[out for out in range(10)] for out in range(10)]
print (full_list)

