"""
    Train the network
"""

import tensorflow as tf
from model import network, BATCH, PREDS, STEPS
from data import get_data

def input_gen():
    """
        Infinite sample generator
    """
    data_in = get_data()
    data = []
    for d in data_in:
        d0 = d[0][:,1:]
        d1 = d[1]
        data.append((d0.resize([STEPS, d0.shape[1]-1])), d1)
    index = 0
    while True:
        index = (index +1)%len(data)
        yield data[index]

def input_fn():
    """
        Estimator input function
    """
    print("Setting up network")
    data = tf.data.Dataset.from_generator(input_gen, (tf.float32, tf.float32), (tf.TensorShape([STEPS, 12]), tf.TensorShape([PREDS])))
    batch = data.shuffle(buffer_size=800).batch(BATCH).make_one_shot_iterator().get_next()
    return {"data": batch[0]}, {"pred": batch[1]}


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    nn = network()
    nn.train(input_fn)
