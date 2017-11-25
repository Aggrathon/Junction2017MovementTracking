"""
    This file contains the neural network model
"""

import tensorflow as tf

BATCH = 32
PREDS = 3
STEPS = 20

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

def model2_fn(features, labels, mode):
    prev_layer = features['data']
    prev_layer = tf.reshape(prev_layer, [-1, 12*STEPS])
    dropout = 0.7 if tf.estimator.ModeKeys.TRAIN else 1.0
    for i in [512, 512, 128, 32]:
        prev_layer = tf.layers.dense(prev_layer, i, activation=tf.nn.relu)
        prev_layer = tf.layers.dropout(prev_layer, dropout)
    output = tf.layers.dense(prev_layer, PREDS, activation=None, name="logits")
    if mode != tf.estimator.ModeKeys.PREDICT:
        with tf.variable_scope("loss"):
            loss = tf.losses.softmax_cross_entropy(labels['pred'], output)
            train = tf.train.AdamOptimizer().minimize(loss, tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(
                mode=mode,
                predictions={'output': tf.arg_max(tf.nn.softmax(output))},
                loss=loss,
                train_op=train
        )
    else:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions={'output': tf.arg_max(tf.nn.softmax(output))}
        )

def network():
    return tf.estimator.Estimator(model_fn, 'network')

def network2():
    return tf.estimator.Estimator(model2_fn, 'network2')
    

if __name__ == "__main__":
    network()
