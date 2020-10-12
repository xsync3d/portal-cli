import sqlite3
from argparse import ArgumentParser, RawTextHelpFormatter

# Just an experimental program

# Connects to database and creates cursor
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# This dictionary will helps us search by column name
column_dict = {
    1: "f_name",
    2: "l_name",
    3: "email",
    4: "address",
    5: "costumer_id"
}


# Everything below this line is bad terrible dumb code

# TODO: create a database interface class and implement "delete column" and "replace row" functions

def decisive_input(question="Are you sure you want to save these changes?"):
    tmp_in = input(question + " Y/N: ")
    if tmp_in.lower() == "y" or tmp_in.lower() == "yes":
        conn.commit()
    elif tmp_in.lower() == "n" or tmp_in.lower() == "no":
        conn.rollback()


def search_costumer(query, column):
    column = column_dict.get(column)
    print(f"searching {query} by {column}")
    # This will definitely end up in a SQL injection later but it will work for now.
    try:
        cursor.execute(f"SELECT * FROM costumers WHERE {column} = {query}")
    except Exception as e:
        print(f"Could not search costumer: {e}")
    result = cursor.fetchmany()
    if not result:
        print("Costumer not found")
        return None
    return result


def create_costumer(*args):
    f_name = args[0]
    l_name = args[1]
    email = args[2]
    # Everything after element 3 is part of the address
    address = ' '.join(args[3:])
    try:
        cursor.execute('INSERT INTO costumers(f_name, l_name, email, address) VALUES (?, ?, ?, ?)',
                       (f_name, l_name, email, address))
    except Exception as e:
        print(f"Could not create costumer: {e}")


def delete_costumer(query, column):
    column = column_dict.get(column)
    if search_costumer(query, column):
        try:
            cursor.execute(f"DELETE FROM costumers WHERE {column}={query}")
            decisive_input()
        except Exception as e:
            print(f"Could not delete costumer: {e}")
    else:
        print("Costumer not found")


def main():
    cursor.execute("SELECT * FROM costumers")

    parser = ArgumentParser(description='mess with dbs or smt idk',
                            usage="use '%(prog)s --help' for more information",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("--search", "-s", help="searches for costumer profile",
                        dest="search_costumer",
                        nargs="+")
    parser.add_argument("--create", "-c",
                        help="creates a new costumer profile\n"
                             "pass arguments as: first name, last name, email, address"
                        , dest="create_costumer", nargs="+")
    parser.add_argument("--delete", "-d",
                        help="deletes costumer profile\n"
                             "pass arguments as: query, column"
                        , dest="delete_costumer", nargs="+")

    args = parser.parse_args()

    print(search_costumer(1, 3))
    if args.search_costumer:
        search_costumer(args.query, args.column)
    if args.create_costumer:
        create_costumer(*args.create_costumer)
    if args.delete_costumer:
        delete_costumer(args.query, args.column)
    # This is for debugging purposes
    cursor.execute("SELECT * FROM costumers")

    print(cursor.fetchall())


if __name__ == "__main__":
    main()
