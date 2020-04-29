from pathlib import Path
from dotenv import load_dotenv
from flask import Flask

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
    for a in os.environ:
        list_env += 'Var: ', a, 'Value: ', os.getenv(a)
    return list_env

if __name__ == "__main__":
    load_dotenv(dotenv_path=env_path)
    app.run()
