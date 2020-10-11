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
    3: "costumer_id"
}


# TODO: create a costumer class

def search_costumer(query, column):
    column = column_dict.get(column)
    print(f"searching {query} by {column}")
    cursor.execute(f"SELECT * FROM costumers WHERE {column}=?", str(query))
    result = cursor.fetchmany()
    if not result:
        print("costumer not found")
        return None
    return result


def create_costumer(*args):
    f_name = args[0]
    l_name = args[1]
    email = args[2]
    address = args[3]
    try:
        cursor.execute('INSERT INTO costumers(f_name, l_name, email, address) VALUES (?, ?, ?, ?)',
                       (f_name, l_name, email, address))
        tmp_in = input("Are you sure you want to save this costumer? Y/N: ")
        if tmp_in.lower() == "y" or tmp_in.lower() == "yes":
            conn.commit()
        else:
            conn.rollback()
    except Exception as e:
        print(f"Could not create costumer: {e}")

def delete_costumer():
    pass


def main():
    cursor.execute("SELECT * FROM costumers")

    parser = ArgumentParser(description='mess with dbs or smt idk',
                            usage="use '%(prog)s --help' for more information",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("--search", "-s", help="search", dest="search_costumer", nargs="+")
    parser.add_argument("--create", "-c", help="creates a new costumer profile", dest="create_costumer", nargs="+")

    args = parser.parse_args()

    print(search_costumer(8, 3))

    if args.search_costumer:
        search_costumer(args.query, args.column)
    if args.create_costumer:
        create_costumer(*args.create_costumer)

    # This is for debugging purposes
    cursor.execute("SELECT * FROM costumers")

    print(cursor.fetchall())


if __name__ == "__main__":
    main()
