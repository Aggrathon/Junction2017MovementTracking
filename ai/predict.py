
from threading import Thread
from queue import Queue
from model import network2
from data import data_smooth, get_next_step


def predict(queue):
    t = Thread(None, _predict, "ai", queue)
    t.start()
    t.join()

def _predict(queue):
    nn = network2()
    def gen():
        global queue
        data = []
        while True:
            while len(data) < 20:
                data.append(queue.get())
                queue.task_done()
            smooth = data_smooth(data)
            start = get_next_step(smooth, 0)
            stop = get_next_step(smooth, start)
            if start > 0 and stop > 0:
                yield data[start:stop]
                data = data[stop:]
    def input()
        data = tf.data.Dataset.from_generator(gen, tf.float32)
        batch = data.make_one_shot_iterator().get_next()
        return {"data": batch}, None
    for res in nn.predict(input):
        print(res['ouput'][0])
