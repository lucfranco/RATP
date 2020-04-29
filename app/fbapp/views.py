import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template
from class_db_mariadb import gestionMARIADB
#import mysql.connector

# Path file .env-----------------
env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

# Config MariaDB--------------------------------
mariadb_config = {
    'user': os.getenv("mariadb_user"),
    'passwd': os.getenv("mariadb_pass"),
    'host': os.getenv("mariadb_host"),
    'database': os.getenv("mariadb_base")
}
# INIT MariaDB------------------------------------
ratp = gestionMARIADB(mariadb_config)

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
@app.route('/index/')
def index():
        return render_template('index.html')


@app.route('/config')
def config():
    list_env = ''
    for i, j in os.environ.items():
        list_env += 'Var: ' + str(i) + ' Value: ' + str(j) + '<br/>'
    return list_env

@app.route('/mysqlshow')
def mysqlshow():
    listStop = ratp.extractRouteGlobal()
    return listStop


if __name__ == "__main__":
    #print(mariadb_config)

    app.run()

