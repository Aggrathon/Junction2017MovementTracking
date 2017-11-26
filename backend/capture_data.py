import json
from flask import Flask, request
import time

app = Flask(__name__)

class LimitedQueue(list):
    def __init__(self, maxlen=100):
        self.maxlen = maxlen + 1

    def append(self, *args): 
        self.extend(args)
        del self[0:len(self) // self.maxlen]

MAX_LIMIT = 100

data = {
    'time': LimitedQueue(MAX_LIMIT),
    'x': LimitedQueue(MAX_LIMIT),
    'y': LimitedQueue(MAX_LIMIT),
    'z': LimitedQueue(MAX_LIMIT)
}

@app.route('/', methods=["POST"])
def index():
    # get and parse json data from request body
    content = request.form
    json_data = json.loads(content["test"])
    timestamp = time.time()
    if 'ArrayGyro' in json_data['Body']:
        coords = json_data['Body']['ArrayGyro'][0]
        data['x'].append(float(coords['x']))
        data['y'].append(float(coords['y']))
        data['z'].append(float(coords['z']))
        data['time'].append(timestamp)
        
    return 'OK', 201


@app.route('/')
def get_data():
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
