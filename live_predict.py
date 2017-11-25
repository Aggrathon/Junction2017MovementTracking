
from queue import Queue
import ai
import backend

QUEUE = Queue()
NAMES = ['174630000602/Meas/Acc/13', '174630000602/Meas/Gyro/13', '174630000495/Meas/Acc/13', '174630000495/Meas/Gyro/13'],
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

if __name__ == "__main__":
    ai.predict.predict(QUEUE)
    backend.PROCESS = process
