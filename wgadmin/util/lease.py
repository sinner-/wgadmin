import ipaddress
from wgadmin.api import app
from wgadmin.db.mysql import query_db
from wgadmin.db.mysql import get_db

def create_leases(lease_subnet):
    try:
        network = ipaddress.ip_network(lease_subnet)
    except ValueError:
        print("Invalid subnet.")
        exit(1)

    with app.app_context():
        for host in list(network.hosts()):
            query_db(
                '''
                INSERT INTO leases(ip)
                VALUES (%s);
                ''',
                (str(host),)
            )
            get_db().commit()
