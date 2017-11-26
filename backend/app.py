#pylint: disable=C0111,W0603,C0103
import json
import time
from flask import Flask, request
from queue import Queue

app = Flask(__name__)

CAPTURE = None
QUEUE = None


@app.route('/<command>')
def start(command):
    global CAPTURE
    global QUEUE
    if command == 'start':
        CAPTURE = ''
    elif command == 'stop':
        with open('data.csv', 'w') as data_file:
            data_file.write(CAPTURE)
        CAPTURE = None
    elif command == 'record':
        QUEUE = ""
    elif command == 'get':
        s = QUEUE
        QUEUE = ""
        return s, 200
    
    return '', 200


@app.route('/', methods=["POST"])
def index():
    global CAPTURE
    global QUEUE

    # get and parse json data from request body
    content = request.form
    data = json.loads(content["data"])
    
    timestamp = str(time.time())
    device_id = data['Uri']
    
    if 'ArrayAcc' in data['Body']:
        data_type = 'ArrayAcc'
        coords = data['Body']['ArrayAcc'][0]

    if 'ArrayGyro' in data['Body']:
        data_type = 'ArrayGyro'
        coords = data['Body']['ArrayGyro'][0]
    
    csv_line = [timestamp, data_type, device_id,
                coords['x'], coords['y'], coords['z']]
    # save data line
    if CAPTURE is not None:
        CAPTURE += ','.join(csv_line) + '\n'
    if QUEUE is not None:
        QUEUE += "%s,%s,%s,%s\n"%(device_id, coords['x'], coords['y'], coords['z'])

    return 'OK', 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
