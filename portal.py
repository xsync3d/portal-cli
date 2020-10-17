#!/usr/bin/env python3
import sqlite3
from argparse import ArgumentParser, RawDescriptionHelpFormatter, RawTextHelpFormatter

# Just an experimental program

# Connects to database and creates cursor
conn = sqlite3.connect("database.db")
cursor = conn.cursor()


# Everything below this line is bad terrible dumb code

# TODO: create a database interface class and implement "delete column" and "replace row" functions

def decisive_input(question="Are you sure you want to save these changes?"):
    tmp_in = input(question + " Y/N: ")
    if tmp_in.lower() == "y" or tmp_in.lower() == "yes":
        conn.commit()
        return True
    elif reply[:1] == "n":
        conn.rollback()


# TODO: further test this function to see if it actually works
def search_customer(query, column):
    # possibly better way to do this https://www.techonthenet.com/mysql/and_or.php?
    query = str(query)
    print(f"searching {query} by {column}")
    try:
        # possible cleanup: split these statements into individual functions
        if column == "1":
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", query)
        elif column == "2":
            cursor.execute("SELECT * FROM customers WHERE f_name = ?", query)
        elif column == "3":
            cursor.execute("SELECT * FROM customers WHERE l_name = ?", query)
        elif column == "4":
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", query)
        elif column == "5":
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", query)
    except Exception as e:
        print(f"Could not find customer: {e}")
    else:
        result = cursor.fetchone()
        if not result:
            print("Customer not found")
            return None
        else:
            return result


def create_customer(*args):
    f_name = args[0]
    l_name = args[1]
    email = args[2]
    # Everything after index 3 is part of the address
    address = ' '.join(args[3:])
    try:
        cursor.execute("INSERT INTO customers(f_name, l_name, email, address) VALUES (?, ?, ?, ?)",
                       (f_name, l_name, email, address))
    except Exception as e:
        print(f"Could not create customer: {e}")


def delete_customer(query, column):
    exists = search_customer(query, column)
    if exists:
        try:
            cursor.execute(f"DELETE FROM customers WHERE {column}={query}")
            decisive_input()
        except Exception as e:
            print(f"Could not delete customer: {e}")
    else:
        print("Customer not found")


def main():
    parser = ArgumentParser(description='mess with dbs or smt idk',
                            usage="use '%(prog)s --help' for more information",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("--search", "-s", help="searches for customer profile", nargs="+")
    parser.add_argument("--create", "-c",
                        help="creates a new customer profile\n"
                             "pass arguments as: first name, last name, email, address", nargs="+")
    parser.add_argument("--delete", "-d",
                        help="deletes customer profile\n"
                             "pass arguments as: query, column", nargs="+")

    args = parser.parse_args()

    if args.search:
        search_customer(args.search[0], args.search[1])
        print(search_customer(args.search[0], args.search[1]))
    if args.create:
        create_customer(*args.create_customer)
    if args.delete:
        delete_customer(args.delete[0], args.delete[1])
    #  print(cursor.fetchall())
    # This is for debugging purposes


# cursor.execute("SELECT * FROM customers")

# print(cursor.fetchall())


if __name__ == "__main__":
    main()
