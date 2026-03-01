import datetime
import json
import random
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time')
def get_time():
    now = datetime.datetime.now()
    filename = f"{now.hour:02}_{now.minute:02}.json"
    with open(f"literature-clock/docs/times/{filename}") as f:
        d = json.load(f)
    return jsonify(random.choice(d))
