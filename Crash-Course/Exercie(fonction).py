# Exercie 1

# Difference

def dif(dig_1, dig_2):
    return (dig_1 - dig_2)
print(dif(2,2))
print(dif(0,2))

# print_day

def print_day(num):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    if num < 1 or num > 7:
        return None
    
    return days[num]
    
print(print_day(3))
print(print_day(41))

# last_element

def last_element(my_list):
    if my_list == []:
        return None

    last_element = my_list[-1]
    return(last_element)

print(last_element([1,2,3,4]))
print(last_element([]))

# number_compare

def number_compare(dig_1,dig_2):
    if dig_1 > dig_2:
        return "First is greater"
    
    elif dig_1 < dig_2:
        return "Second is greater"
    
    else:
        return "Numbers are equal"
    
print(number_compare(1,1))
print(number_compare(1,2)) 
print(number_compare(2,1))

# single_letter_count

def single_letter_count(string, lettre):
    string = string.lower()
    lettre = lettre.lower()
    single_letter_count = string.count(lettre)

    if string.count(lettre) == 0:
        return "0"
    
    return single_letter_count

print(single_letter_count("amazing","A"))

# multiple_letter_count

def multiple_letter_count(word):
    result = {}

    # for letter in word:
    #     result[letter] = 1

    for letter in word:
        if letter in result:
            result[letter] = result[letter] + 1
        else:
            result[letter] = 1
    
    return result 
        
print(multiple_letter_count("hello"))
print(multiple_letter_count("person"))

# list_manipulation

def list_manipulation(list, command, location, value=None):
   
   if command == "remove":
       if location == "end":
           return list.pop()
       elif location == "beginning":
           return list.pop(0)
       
   elif command == "add":
       if location == "beginning":
           list.insert(0,value)
           return list
       elif location == "end":
           list.append(value)
           return list

print(list_manipulation([1,2,3], "remove", "end"))
print(list_manipulation([1,2,3], "remove", "beginning"))
print(list_manipulation([1,2,3], "add", "beginning", 20)) 
print(list_manipulation([1,2,3], "add", "end", 30)) 

# is_palindrome

def is_palindrome(word):
    word = word.lower()
    word = word.replace(" ","")
    
    if word == word[::-1]:
        return True
    else:
        return False
    
print(is_palindrome('testing'))
print(is_palindrome('tacocat'))
print(is_palindrome('hannah')) 
print(is_palindrome('robert'))
print(is_palindrome('a man a plan a canal Panama'))
    
# frequency

def frequency(list, search_term):
    list.count(search_term)
    return list.count(search_term)

print(frequency([1,2,3,4,4,4], 4))
print(frequency([True, False, True, True], False))

# flip_case 

def flip_case(string, letter):
     result = ""

     for let in string:
        if let.lower() == letter.lower():
            result += let.swapcase()
        else:
            result += let
    
     return result

print(flip_case("Hardy har har", "h"))
    

  
# multiply_even_numbers

def multiply_even_numbers(list):
    even = [lis for lis in list if lis % 2 == 0]
    result = 1
    result = result * even

    return result
    
print(multiply_even_numbers([2,3,4,5,6]))

# mode

def mode(list):

    result = {}
    for dig in list:
        if dig in result:
            result[dig] += 1
        else:
            result[dig] = 1
    
    most_commun = None
    highest_result = 0

    for dig in result:
        if result[dig] > highest_result:
            highest_result = result[dig]
            most_commun = dig

    return most_commun

print(mode([2,4,1,2,3,3,4,4,5,4,4,6,4,6,7,4]))
    
            
        
        

# captitalize

def capitalize(string):
    word = string[0].upper() + string[1:]
    return word
print(capitalize("tim"))
print(capitalize("matt"))

# compact

def compact(list):
    return[lis for lis in list if lis]

print(compact([0,1,2,"",[], False, {}, None, "All done"]))

# partition

def partition(lst, callback):
    true_list = []
    false_list = []
    
    for item in lst:
        if callback(item):
            true_list.append(item)
        else:
            false_list.append(item)
    
    return [true_list, false_list]
def is_even(num):
    return num % 2 == 0

print(partition([1,2,3,4], is_even))
    


# intersection

def intersection(lis_1, lis_2):
    result = []
    for lis in lis_1:
        if lis in lis_2:
            result.append(lis)

    return result
        
print(intersection([1,2,3], [2,3,4]))

# once

def once(fn):
    def inner(x, y):
        if inner.called:
            return None
        inner.called = True
        return fn(x, y)
    
    inner.called = False
    return inner


def add(a, b):
    return a + b

add = once(add) 

print(add(2,2))
print(add(2,20)) 
print(add(12,20))


# Exercice 2

def solution(string):
    return string[::-1]




import math

def new_avg(arr, newavg):
    n = len(arr) + 1
    required_total = newavg * n
    needed = required_total - sum(arr)
    
    if needed <= 0:
        raise ValueError("Expected New Average is too low")
    
    return math.ceil(needed)


def sequence_sum(begin, end, step):
    if begin > end:
        return 0
    return sum(range(begin, end + 1, step))


def max_diff(lst):
    if not lst:
        return 0
    return max(lst) - min(lst)


def count_smileys(arr):
    eyes = [":", ";"]
    noses = ["-", "~"]
    mouths = [")", "D"]
    
    count = 0
    
    for face in arr:
        if len(face) == 2:
            if face[0] in eyes and face[1] in mouths:
                count += 1
        elif len(face) == 3:
            if face[0] in eyes and face[1] in noses and face[2] in mouths:
                count += 1
                
    return count



def count_sentences(text):
    return text.count(".") + text.count("!") + text.count("?")


def race(v1, v2, g):
    if v1 >= v2:
        return None
    
    time = g * 3600 / (v2 - v1)
    
    hours = int(time // 3600)
    minutes = int((time % 3600) // 60)
    seconds = int(time % 60)
    
    return [hours, minutes, seconds]


def shifted_diff(first, second):
    if len(first) != len(second):
        return -1
    
    for i in range(len(first)):
        if first[i:] + first[:i] == second:
            return i
    return -1