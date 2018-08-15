from wgadmin.api import app
from wgadmin.db.mysql import query_db
from wgadmin.db.mysql import get_db

def set_admin(username):
    with app.app_context():
        query_db(
            '''
            UPDATE users
            SET role="admin"
            WHERE username=%s;
            ''',
            (username,)
        )
        get_db().commit()
