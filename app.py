import datetime
import json
import random
import subprocess
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

@app.route('/brightness/<int:value>')
def set_brightness(value):
    value = max(0, min(255, value))
    try:
        subprocess.run(
            ['sudo', 'tee', '/sys/class/backlight/10-0045/brightness'],
            input=str(value).encode(),
            check=True
        )
        return jsonify({'brightness': value})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
