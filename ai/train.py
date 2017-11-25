"""
    Train the network
"""

import tensorflow as tf
import numpy as np
from model import network, BATCH, PREDS, STEPS

def input_gen():
    #TODO read files
    #TODO find footsteps
    #TODO create sequences
    while True:
        yield np.zeros([STEPS, 12], np.float), np.zeros([PREDS], np.float)

def input_fn():
    data = tf.data.Dataset.from_generator(input_gen, (tf.float32, tf.float32), (tf.TensorShape([STEPS, 12]), tf.TensorShape([PREDS])))
    batch = data.shuffle(buffer_size=800).batch(BATCH).make_one_shot_iterator().get_next()
    return {"data": batch[0]}, {"pred": batch[1]}


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    nn = network()
    nn.train(input_fn)
