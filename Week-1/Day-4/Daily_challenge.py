menu = {
    "espresso": 7.0,
    "latte": 12.0,
    "cappuccino": 10.0
}

def show_menu(menu_dict):
    if menu_dict == "":
        print("The menu is empty")
    else:
        for drink, price in menu_dict.items():
            print(f"{drink} - {price}₪")
    


def Add_item(menu_dict):
    drink_name = input("Enter new drink name: ")

    if drink_name in menu_dict:
        print("Item already exists!")
    else:
        price = float(input("Enter a price"))
        menu_dict[drink_name] = price
        print(f"{drink_name} added!")

    

def update_price(menu_dict):
    drink = input('which drink do you want to update')

    if drink in menu_dict:
        price = float(input("Give me a new price: "))
        menu_dict[drink] = price
        print("Price updated!")
    else:
        print('item not found')


def delete_item(menu_dict):
    drink = input("Which drink do you wan to remove? : ")

    if drink in menu_dict:
        menu.pop(drink)
        print("Item deleted.")
    else:
        print("Item not found.")


def show_options():
    print("What would you like to do?")
    print("1. Show menu")
    print("2. Add item")
    print("3. Update price")
    print("4. Delete item")
    print("5. Exit")


def run_coffee_shop():
    while True:
        show_options()
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            show_menu(menu)
        elif choice == "2":
            Add_item(menu)
        elif choice == "3":
            update_price(menu)
        elif choice == "4":
            delete_item(menu)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

run_coffee_shop()

