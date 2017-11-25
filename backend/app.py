#pylint: disable=C0111,W0603,C0103
import json
import time
from flask import Flask, request

app = Flask(__name__)

CAPTURE = None


@app.route('/<command>')
def start(command):
    global CAPTURE
    if command == 'start':
        CAPTURE = ''
    if command == 'stop':
        with open('data.csv', 'w') as data_file:
            data_file.write(CAPTURE)
        CAPTURE = None
    
    return '', 200


@app.route('/', methods=["POST"])
def index():
    global CAPTURE

    content = request.form
    data = json.loads(content["data"])
    timestamp = str(time.time())
    coords = data['Body']['ArrayAcc'][0]
    csv_line = [timestamp, coords['x'], coords['y'], coords['z']]
    if CAPTURE:
        CAPTURE += ','.join(csv_line) + '\n'

    return ','.join(csv_line) + '\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
