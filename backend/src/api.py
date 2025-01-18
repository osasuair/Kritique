import time
from flask import Flask

app = Flask(__name__)

# Dummy API endpoint
@app.route('/time')
def get_current_time():
    return {'time': time.time()}
