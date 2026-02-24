# 1. Ask for user input
user_string = input("Enter a string of exactly 10 characters: ")

# 2. Check the length
if len(user_string) < 10:
    print("String not long enough.")
elif len(user_string) > 10:
    print("String too long.")
else:
    print("Perfect string")
    
    # 3. Print first and last characters
    print("First character:", user_string[0])
    print("Last character:", user_string[-1])
    
    # 4. Build the string character by character
    for i in range(1, len(user_string) + 1):
        print(user_string[:i])