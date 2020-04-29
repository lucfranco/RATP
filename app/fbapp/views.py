import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
import mysql.connector

# Path file .env-----------------
env_path = Path.cwd() / '.env'

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
def index():
        return "Hello world !" + str(env_path)


@app.route('/config')
def config():
    list_env = ''
    for i, j in os.environ.items():
        list_env += 'Var: ' + str(i) + ' Value: ' + str(j) + '<br/>'
    return list_env

@app.route('/mysqlshow')
def mysqlshow():
    mariadb = mysql.connector.connect(**mariadb_config)
    route_global = mariadb.cursor()
    request = ("SELECT DISTINCT LEFT(MD5(RAND()), 16) AS id, route_short_name FROM routes GROUP BY route_short_name ORDER BY route_short_name LIMIT 0,3")
    print("1| " + request)
    route_global.execute(request)
    records = route_global.fetchall()
    print(records)
    print(route_global.rowcount)
    return records


if __name__ == "__main__":
    load_dotenv(dotenv_path=env_path)

    # Config MariaDB--------------------------------
    mariadb_config = {
        'user': os.getenv("mariadb_user"),
        'passwd': os.getenv("mariadb_pass"),
        'host': os.getenv("mariadb_host"),
        'database': os.getenv("mariadb_base")
    }
    #print(mariadb_config)

    app.run()

