import argparse
from wgadmin.db.mysql import create_tables
from wgadmin.db.mysql import drop_tables

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",
                        "--create-tables",
                        action="store_true",
                        dest="createtables")
    parser.add_argument("-d",
                        "--drop-tables",
                        action="store_true",
                        dest="droptables")
    args = parser.parse_args()

    if args.droptables:
        print("Dropping all tables from database.")
        drop_tables()

    if args.createtables:
        print("Creating wgadmin tables from schema.")
        create_tables()
