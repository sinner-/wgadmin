import argparse
from wgadmin.api import app
from wgadmin.db.mysql import create_tables
from wgadmin.db.mysql import drop_tables
from wgadmin.util.lease import create_leases
from wgadmin.util.admin import set_admin

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
    parser.add_argument("-a",
                        "--set-admin-user",
                        action="store_true",
                        dest="setadminuser")
    parser.add_argument("-u",
                        "--username",
                        type=str,
                        dest="username")

    args = parser.parse_args()

    if args.droptables:
        print("Dropping all tables from database.")
        drop_tables()

    if args.createtables:
        print("Creating wgadmin tables from schema.")
        create_tables()

    elif args.createleases:
        if not args.lease_subnet:
            print("You must call --create-leases with --lease-subnet.")
            exit(1)

        create_leases(args.lease_subnet)

    elif args.setadminuser:
        if not args.username:
            print("You must clal --set-admin-user with --username.")
            exit(1)

        set_admin(args.username)

    else:
        parser.print_help()
