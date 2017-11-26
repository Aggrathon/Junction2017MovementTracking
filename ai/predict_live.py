
from threading import Thread
import urllib.request
from model import network2
from data import data_smooth, get_next_step
from queue import Queue
import json
import time
from flask import Flask, request
import tensorflow as tf
from time import sleep

app = Flask(__name__)

NAMES = ['174630000602/Meas/Acc/13', '174630000602/Meas/Gyro/13', '174630000495/Meas/Acc/13', '174630000495/Meas/Gyro/13']
POS = {n: i for i, n in enumerate(NAMES)}
POST = [None for _ in NAMES]

def process(name, x, y, z):
    global POST
    global NAMES
    global POS
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
        return line
    return None

def predict():
    nn = network2()
    def gen():
        data = []
        while True:
            while len(data) < 20:
                sleep(0.5)
                webURL = urllib.request.urlopen("http://0.0.0.0:5000/get")
                response_data = webURL.read()
                encoding = webURL.info().get_content_charset('utf-8')
                data = response_data.decode(encoding)
                for line in data.split('\n'):
                    if line:
                        split = line.split(',')
                        d = process(split[0], float(split[1]), float(split[2]), float(split[3]))
                        if d:
                            data.append(d)
                            print("Added data")
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
    key = ['straight', 'left', 'right', 'stairs up', 'stairs down', 'normal', 'problem']
    for res in nn.predict(input):
        print("PREDICTION:  ", '\t'.join('%s: %.0f%%'%(k,r*100.0) for k, r in zip(key, res['output'])))


if __name__ == "__main__":
    urllib.request.urlopen("http://0.0.0.0:5000/record").read()
    predict()
