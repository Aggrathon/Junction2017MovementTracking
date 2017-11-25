"""
    This file contains the neural network model
"""

import tensorflow as tf

BATCH = 32
PREDS = 4
STEPS = 100

def model_fn(features, labels, mode):
    data = features['data']
    dropout = 0.9 if tf.estimator.ModeKeys.TRAIN else 1.0
    lstm = tf.nn.rnn_cell.MultiRNNCell([
        tf.contrib.rnn.LayerNormBasicLSTMCell(size, dropout_keep_prob=dropout)
        for size in [30, 30 , 30, 30, 30]])
    state = lstm.zero_state(BATCH, tf.float32)
    for i in range(STEPS):
        output, state = lstm(data[:,i,:], state)
    output = tf.layers.dense(output, PREDS, activation=None, name="logits")
    if mode != tf.estimator.ModeKeys.PREDICT:
        with tf.variable_scope("loss"):
            loss = tf.losses.softmax_cross_entropy(labels['pred'], output)
            train = tf.train.AdamOptimizer().minimize(loss, tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(
                mode=mode,
                predictions={'output': tf.nn.softmax(output)},
                loss=loss,
                train_op=train
        )
    else:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions={'output': tf.nn.softmax(output)}
        )


def network():
    return tf.estimator.Estimator(model_fn, 'network')
    

if __name__ == "__main__":
    network()
