#!/usr/bin/env python3
import sqlite3
from argparse import ArgumentParser, RawDescriptionHelpFormatter, RawTextHelpFormatter

# Connects to database and creates cursor
conn = sqlite3.connect("database.db")
cursor = conn.cursor()


# TODO: create a database interface class and implement "delete column" and "replace row" functions

def query_user(question: str = "Are you sure you want to save these changes?") -> bool:
    reply = input(question + " Y/N : ").lower().strip()
    if reply[:1] == "y":
        conn.commit()
        return True
    elif reply[:1] == "n":
        conn.rollback()
        return False
    else:
        print("Invalid input...")
        query_user(question)


# TODO: further test this function to see if it actually works
def search_customer(column: str, query: str) -> tuple:
    # possibly better way to do this https://www.techonthenet.com/mysql/and_or.php?
    query = str(query)
    print(f"searching {query} by {column}")
    # This will definitely end up in a SQL injection later but it will work for now.
    try:
        # possible cleanup: split these statements into individual functions
        if column == "1":
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", query)
        elif column == "2":
            cursor.execute("SELECT * FROM customers WHERE f_name = ?", query)
        elif column == "3":
            cursor.execute("SELECT * FROM customers WHERE l_name = ?", query)
        elif column == "4":
            cursor.execute("SELECT * FROM customers WHERE email = ?", query)
        elif column == "5":
            cursor.execute("SELECT * FROM customers WHERE address = ?", query)
    except Exception as e:
        print(f"Could not find customer: {e}")
    else:
        result = cursor.fetchone()
        if not result:
            print("Customer not found")
            return None
        else:
            return result


def create_customer(*args: tuple):
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


def delete_customer(column: str, query: str):
    exists = search_customer(column, query)
    if exists:
        try:
            cursor.execute("DELETE FROM customers WHERE customer_id = ?", str(exists[0]))
            query_user()
        except Exception as e:
            print(f"Could not delete customer: {e}")
    else:
        print("Customer not found")


def print_all_customers():
    cursor.execute("SELECT * FROM customers")
    print(cursor.fetchall())


def main():
    parser = ArgumentParser(description='mess with dbs or smt idk',
                            usage="use '%(prog)s --help' for more information",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("--search", "-s",
                        help="searches for customer profile\n"
                             "pass arguments as: column, query", nargs="+")
    parser.add_argument("--create", "-c",
                        help="creates a new customer profile\n"
                             "pass arguments as: first name, last name, email, address", nargs="+")
    parser.add_argument("--delete", "-d",
                        help="deletes customer profile\n"
                             "pass arguments as: column, query", nargs="+")
    parser.add_argument("-pac", help="print all customer profiles", action="store_true")

    args = parser.parse_args()

    if args.search:
        search_customer(args.search[0], args.search[1])
        print(search_customer(args.search[0], args.search[1]))
    if args.create:
        create_customer(*args.create_customer)
    if args.delete:
        delete_customer(args.delete[0], args.delete[1])
    if args.pac:
        print_all_customers()


if __name__ == "__main__":
    main()
