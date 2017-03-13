from os import system
from databasing import conn, cursor, close_connection, write_csv_to_database


def clear():
    system('clear')


def return_to_menu():
    input("\nHit ENTER to return to menu.")
    return ui(cursor)


def check_content(cursor):
    cursor.execute("SELECT * FROM life_saver;")
    current = cursor.fetchone()
    if not current:
        return True


def look_up_record(cursor):
    search = input("What bill are you looking for? ")
    cursor.execute("SELECT * FROM life_saver WHERE LOWER(bill) = %s",
                   (search.lower(), ))
    try:
        result = cursor.fetchone()
        print('\nBill: ' + search)
        print("Amount: ", result[2])
        print("Month due:", result[3])
        print("Day due:", result[4])
    except TypeError:
        print("Bill not found. Try again!")
        return_to_menu()
    return_to_menu()


def add_record(cursor):
    bill = input("What is the bill for? ")
    amount = input("How much is the bill? $")
    print("When is it due?")
    month = input("Month: ")
    day = int(input("Day: "))
    cursor.execute("INSERT INTO life_saver(bill, amount, month, day) VALUES (%s, %s, %s, %s)", (bill, amount, month, day))
    print("Added {} bill to database.".format(bill))
    return_to_menu()


def show_record(cursor):
    cursor.execute("SELECT * FROM life_saver;")
    current = cursor.fetchone()
    while current:
            print(current)
            current = cursor.fetchone()


def delete_record(cursor):
    show_record(cursor)
    id = int(input("\nEnter ID field to delete: "))
    confirm = input("Confirm delete: Y/n ")
    if confirm.lower() == 'y':
        cursor.execute("DELETE FROM life_saver WHERE id = %s", (id,))
        print("Deleted ID #{} from database.".format(id))
        return_to_menu()
    else:
        print("Nothing deleted.")
        return_to_menu()


def update_record(cursor):
    show_record(cursor)
    value_to_update = int(input("\nEnter ID to update: "))
    which_column = input("Which column (bill(1), amount(2), month(3), day(4))? ")
    while True:
        if which_column == "1":
            which_column = 'bill'
            break
        elif which_column == "2":
            which_column = 'amount'
            break
        elif which_column == "3":
            which_column = 'month'
            break
        elif which_column == "4":
            which_column = 'day'
            break
    to_what = input("To what? ")
    cursor.execute("UPDATE life_saver SET {} = %s WHERE id = %s".format(which_column), (to_what, value_to_update,))
    if type(to_what) is float:
        print("Updated {} of ID #{} to ${}.".format(which_column, value_to_update, to_what))
    else:
        print("Updated {} of ID #{} to {}.".format(which_column, value_to_update, to_what))
    return_to_menu()


def ui(cursor):
    clear()
    print("\t== ~ == Welcome to the bills and budgets interaction menu == ~ ==\n\nHere are your options:\n")
    print("\t1) Look up a bill by name.")
    print("\t2) Add a bill.")
    print("\t3) Delete row from bills.")
    print("\t4) Update a bill.")
    print("\t5) Show bills.")
    print("\t6) Quit.")
    choice = input("\nChoose from menu: ")
    print(" ")
    if choice == '1':
        look_up_record(cursor)
    elif choice == '2':
        add_record(cursor)
    elif choice == '3':
        delete_record(cursor)
    elif choice == '4':
        update_record(cursor)
    elif choice == '5':
        show_record(cursor)
        return_to_menu()
    elif choice == '6':
        print("Saved state. See you next time!\n")
        close_connection(conn, cursor)
    else:
        ui(cursor)


if __name__ == '__main__':
    if check_content(cursor):
        write_csv_to_database()
    ui(cursor)
