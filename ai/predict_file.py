
import sys
import tensorflow as tf
import numpy as np
from model import network2, STEPS
from data import get_data

FILE = 'data/jonas_left_fix.csv'
def input_gen():
    """
        sample generator
    """
    data_in = get_data([FILE])
    data = []
    for d in data_in:
        d0 = np.zeros((STEPS, 12), np.float)
        length = min(STEPS, d[0].shape[0])
        d0[:length,:] = d[0][:length,:]
        d1 = d[1]
        data.append((d0, d1))
    for d in data:
        yield d

def predict():
    nn = network2()
    def input():
        data = tf.data.Dataset.from_generator(input_gen, (tf.float32, tf.float32))
        batch = data.make_one_shot_iterator().get_next()
        return {"data": batch[0]}, None
    key = ['straight', 'left', 'right', 'stairs up', 'stairs down', 'normal', 'problem']
    for res in nn.predict(input):
        print("PREDICTION:  ", '\t'.join('%s: %.0f%%'%(k,r*100.0) for k, r in zip(key, res['output'])))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        FILE = sys.argv[1]
    predict()
