from wgadmin.api import app
from wgadmin.common.config import CONF

def main():
    app.run(debug=CONF.debug)
