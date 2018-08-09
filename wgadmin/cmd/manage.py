import argparse
from wgadmin.api import app
from wgadmin.db.mysql import create_tables
from wgadmin.db.mysql import drop_tables
from wgadmin.util.lease import create_leases

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
    parser.add_argument("-l",
                        "--create-leases",
                        action="store_true",
                        dest="createleases")
    parser.add_argument("-s",
                        "--lease-subnet",
                        type=str,
                        dest="lease_subnet")

    args = parser.parse_args()

    if args.droptables:
        print("Dropping all tables from database.")
        drop_tables()

    elif args.createtables:
        print("Creating wgadmin tables from schema.")
        create_tables()

    elif args.createleases:
        if not args.lease_subnet:
            print("You must call --create-leases with --lease-subnet.")
            exit(1)

        create_leases(args.lease_subnet)
    else:
        parser.print_help()
