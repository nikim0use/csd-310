# Title: what_a_book.py
# Author: Kristin Bougrine
# Date: February 22, 2023
# Description: WhatABook program; Console program that interfaces with a MySQL database

#import statements
import sys
import mysql.connector
from mysql.connector import errorcode

#database config object
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

def show_menu():
    print("\n  -- Main Menu --")

    print("    1. View Books\n    2. View Store Locations\n    3. My Account\n    4. Exit Program")

    try:
        choice = int(input('      <Example enter: 1 for book listing>: '))

        return choice
    except ValueError:
        print("\n  Invalid number, program terminated...\n")

        sys.exit(0)

def show_books(_cursor):
    # inner join query 
    _cursor.execute("SELECT book_id, book_name, author, details from book")

    # get results from the cursor object 
    books = _cursor.fetchall()

    print("\n  -- DISPLAYING AVAILABLE BOOKS --")
    
    # iterate over the data set and display the results 
    for book in books:
        print("  Book ID: {}\n  Book Name: {}\n  Author: {}\n  Details: {}\n".format(book[0], book[1], book[2], book[3]))

def show_locations(_cursor):
    _cursor.execute("SELECT store_id, locale from store")

    locations = _cursor.fetchall()

    print("\n  -- DISPLAYING OUR STORE LOCATIONS --")

    for location in locations:
        print("  Locale: {}\n".format(location[1]))

def validate_user():
    #validate users ID

    try:
        user_id = int(input('\n      Enter a customer id <Example 1 for user_id 1>: '))

        if user_id < 0 or user_id > 3:
            print("\n  Invalid customer number, program terminated...\n")
            sys.exit(0)

        return user_id
    except ValueError:
        print("\n  Invalid number, program terminated...\n")

        sys.exit(0)

def show_account_menu():
    #display user account menu

    try:
        print("\n      -- Customer Menu --")
        print("        1. Wishlist\n        2. Add Book\n        3. Main Menu")
        account_option = int(input('        <Example enter: 1 for wishlist>: '))

        return account_option
    except ValueError:
        print("\n  Invalid number, program terminated...\n")

        sys.exit(0)

def show_wishlist(_cursor, _user_id):
    #query database for a list of books added to user wishlist

    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(_user_id))
    
    wishlist = _cursor.fetchall()

    print("\n        -- DISPLAYING WISHLIST ITEMS --")

    for book in wishlist:
        print("        Book Name: {}\n        Author: {}\n".format(book[4], book[5]))

def show_books_to_add(_cursor, _user_id):
    #query database for a list of books not in user wishlist

    query = ("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))

    print(query)

    _cursor.execute(query)

    books_to_add = _cursor.fetchall()

    print("\n        -- DISPLAYING AVAILABLE BOOKS --")

    for book in books_to_add:
        print("        Book Id: {}\n        Book Name: {}\n".format(book[0], book[1]))

def add_book_to_wishlist(_cursor, _user_id, _book_id):
    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(_user_id, _book_id))

try:
    #try/catch block for handling potential MySQL database errors

    db = mysql.connector.connect(**config) # connect to WhatABook database

    cursor = db.cursor() # cursor for MySQL queries

    print("\n  Welcome to the WhatABook Application! ")

    user_selection = show_menu() # show main menu

    # while user's selection is not 4
    while user_selection != 4:

        # if user selects option 1, call show_books method and display books
        if user_selection == 1:
            show_books(cursor)

        # if user selects option 2, call show_locations method and display configured locations
        if user_selection == 2:
            show_locations(cursor)

        # if user selects option 3, call validate_user method to validate entered user_id
        # call show_account_menu() to show account settings menu
        if user_selection == 3:
            my_user_id = validate_user()
            account_option = show_account_menu()

            # while account option does not equal 3
            while account_option != 3:

                # if user selects option 1, call show_wishlist() method to show current users
                # configured wishlist items
                if account_option == 1:
                    show_wishlist(cursor, my_user_id)

                # if user select option 2, call the show_books_to_add function to show user
                # books not currently configured in users wishlist
                if account_option == 2:

                    # show books not currently configured in users wishlist
                    show_books_to_add(cursor, my_user_id)

                    # get entered book_id 
                    book_id = int(input("\n        Enter the id of the book you want to add: "))
                    
                    # add selected book to users wishlist
                    add_book_to_wishlist(cursor, my_user_id, book_id)

                    db.commit() # commit the changes to the database 

                    print("\n        Book id: {} was added to your wishlist!".format(book_id))

                # if selected option is less than 0 or greater than 3, display invalid user selection 
                if account_option < 0 or account_option > 3:
                    print("\n      Invalid option, please retry...")

                # show account menu 
                account_option = show_account_menu()
        
        # if user selection less than 0 or greater than 4, display invalid user selection
        if user_selection < 0 or user_selection > 4:
            print("\n      Invalid option, please retry...")
            
        # show the main menu
        user_selection = show_menu()

    print("\n\n  Program terminated...")

except mysql.connector.Error as err:
    #handle errors

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    #close connection to MySQL

    db.close()

#Adapted from Professor Krasso's Code