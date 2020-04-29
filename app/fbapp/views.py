from pathlib import Path
from dotenv import load_dotenv
from flask import Flask


env_path = Path.cwd() / '.env'
#env_path = "../../.env"
print('env_path' + str(env_path))

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
def index():
        return "Hello world !" + str(env_path)

if __name__ == "__main__":
    load_dotenv(dotenv_path=env_path)
    app.run()
