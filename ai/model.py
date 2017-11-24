"""
    This file contains the neural network model
"""

import tensorflow as tf

BATCH = 32
PREDS = 4

def model_fn(features, labels, mode):
    data = features['data']
    dropout = 0.9 if tf.estimator.ModeKeys.TRAIN else 1.0
    lstm = tf.nn.rnn_cell.MultiRNNCell([
        tf.nn.rnn_cell.DropoutWrapper(tf.nn.rnn_cell.LSTMCell(size), dropout, dropout)
        for size in [30, 30 , 30, 30, 30]])
    state = lstm.zero_state(batch_size, tf.float32)
    for i in range(steps):
        output, state = lstm(data[:,i], state)
    output = tf.layers.dense(output, [BATCH, PREDS], activation=None)
    if mode != tf.estimator.ModeKeys.PREDICT:
        with tf.variable_scope("loss"):
            loss = tf.losses.softmax_cross_entropy(labels['pred'], output)
            train = tf.trainer.AdamOptimizer().minimize(loss, tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(
                mode=mode,
                predictions={'output': tf.softmax(output)},
                loss=loss,
                train_op=train
        )
    else:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions={'output': tf.softmax(output)}
        )
    
    
def network():
    return tf.estimator.Estimator(model_fn, 'network')
        

if __name__ == "__main__":
    network()

