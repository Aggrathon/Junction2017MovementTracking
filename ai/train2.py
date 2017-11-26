"""
    Train the network
"""

import tensorflow as tf
from model import network2
from train import input_fn

if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    nn = network2()
    nn.train(input_fn, None, 10000)
