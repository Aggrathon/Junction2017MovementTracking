
from threading import Thread
from model import network2
from data import data_smooth, get_next_step
from queue import Queue
import json
import time
from flask import Flask, request
import tensorflow as tf

app = Flask(__name__)

QUEUE = Queue()
NAMES = ['174630000602/Meas/Acc/13', '174630000602/Meas/Gyro/13', '174630000495/Meas/Acc/13', '174630000495/Meas/Gyro/13']
POS = {n: i for i, n in enumerate(NAMES)}
POST = [None for _ in NAMES]

def process(name, x, y, z):
    global POST
    global NAMES
    global POS
    global QUEUE
    POST[POS[name]] = [x, y, z]
    fin = True
    for p in POST:
        if p is None:
            fin = False
            break
    if fin:
        line = []
        for p in POST:
            for o in p:
                line.append(o)
        POST = [None for _ in NAMES]
        QUEUE.put(line)

@app.route('/', methods=["POST"])
def index():
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
    
    process(device_id, float(coords['x']), float(coords['y']), float(coords['z']))
    return 'OK', 201


def predict():
    t = Thread(None, _predict, "ai")
    t.start()

def _predict():
    nn = network2()
    def gen():
        global QUEUE
        data = []
        while True:
            while len(data) < 20:
                data.append(QUEUE.get())
                QUEUE.task_done()
            smooth = data_smooth(data)
            start = get_next_step(smooth, 0)
            stop = get_next_step(smooth, start)
            if start > 0 and stop > 0:
                yield data[start:stop]
                data = data[stop:]
    def input():
        data = tf.data.Dataset.from_generator(gen, tf.float32)
        batch = data.make_one_shot_iterator().get_next()
        return {"data": batch}, None
    for res in nn.predict(input):
        print("#################", "PREDICTION:", res['ouput'][0], "#################")


if __name__ == "__main__":
    predict()
    app.run(host='0.0.0.0', debug=True)
