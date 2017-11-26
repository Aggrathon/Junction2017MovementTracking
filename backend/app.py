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
    if command == 'stop':#pylint: disable=C0111,W0603,C0103
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
        filename = "data_{:s}.csv".format(str(time.time()))
        with open(filename, 'w') as data_file:
            data_file.write(CAPTURE)
        CAPTURE = None
    
    return '', 200


@app.route('/', methods=["POST"])
def index():
    global CAPTURE

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
    if CAPTURE:
        CAPTURE += ','.join(csv_line) + '\n'

    return 'OK', 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
            data_file.write(CAPTURE)
        CAPTURE = None
    
    return '', 200


@app.route('/', methods=["POST"])
def index():
    global CAPTURE

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
    if CAPTURE:
        CAPTURE += ','.join(csv_line) + '\n'

    return 'OK', 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
