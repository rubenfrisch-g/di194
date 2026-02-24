def get_age(year, month, day):
    current_year = 2026
    current_month = 2
    age = current_year - year

    if current_month < month:
        age -= 1

def can_retire(gender, date_of_birth):
    year, month, day = date_of_birth

    age = get_age(year, month, day)

    if gender == "m":
        return age >= 67
    elif gender == "f":
        return age >= 62
    else:
        return False
    
gender = input("Enter your gender (m/f): ")
dob = input("Enter your date of birth (yyyy/mm/dd): ")

year, month, day = dob.split("/")
year = int(year)
month = int(month)
day = int(day)

retire = can_retire(gender, (year, month, day))

if retire:
    print("You can retire.")
else:
    print("You cannot retire yet.")
    




