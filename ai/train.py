"""
    Train the network
"""

import tensorflow as tf
import numpy as np
from model import network, BATCH, PREDS, STEPS
from data import get_data

def input_gen():
    """
        Infinite sample generator
    """
    data_in = get_data()
    data = []
    for d in data_in:
        for i in range(3):
            d0 = np.zeros((STEPS, 12), np.float)
            length = min(STEPS, d[0].shape[0]-2)
            d0[:length,:] = d[0][i:length+i,:]
            d1 = d[1]
            data.append((d0, d1))
    index = 0
    while True:
        index = (index +1)%len(data)
        yield data[index]

def input_fn():
    """
        Estimator input function
    """
    print("Setting up network")
    data = tf.data.Dataset.from_generator(input_gen, (tf.float32, tf.float32))
    batch = data.shuffle(buffer_size=800).batch(BATCH).make_one_shot_iterator().get_next()
    return {"data": batch[0]}, {"pred": batch[1]}


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    nn = network()
    nn.train(input_fn)
