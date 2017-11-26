import os
import sys
import tensorflow as tf
from tensorflow.python.tools.freeze_graph import freeze_graph
from tensorflow.python.tools.optimize_for_inference_lib import optimize_for_inference
from model import model2_fn as model_fn

EXPORT_FOLDER = os.path.join('export')
INPUT_TENSOR_NAME = 'input'
OUTPUT_TENSOR_NAME = 'output'
EXPORTED_MODEL_NAME = os.path.join(EXPORT_FOLDER, 'model.pb')

def get_session():
    sess = tf.Session()
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    ckpt = tf.train.get_checkpoint_state('network2')
    saver.restore(sess, ckpt.model_checkpoint_path)
    return sess

def get_latest_export():
    for s in sorted(os.listdir(EXPORT_FOLDER), reverse=True):
        path = os.path.join(EXPORT_FOLDER, s)
        if os.path.isdir(path):
            print('Loading exported model', s)
            return path
    return EXPORT_FOLDER

def export():
    tf.logging.set_verbosity(tf.logging.INFO)
    inp = tf.placeholder(tf.float32, [None], name=INPUT_TENSOR_NAME)
    model_fn(dict(data=inp), None, tf.estimator.ModeKeys.PREDICT)
    sess = get_session()
    tf.train.Saver().save(sess, os.path.join(EXPORT_FOLDER, 'checkpoint.ckpt'))
    tf.train.write_graph(sess.graph_def, EXPORT_FOLDER, 'graph.pbtxt', True)
    sess.close()
    print("Freezing graph")
    lp = get_latest_export()
    ckpt = tf.train.get_checkpoint_state(EXPORT_FOLDER)
    freeze_graph(
        os.path.join(EXPORT_FOLDER, 'graph.pbtxt'),
        None,
        False,
        ckpt.model_checkpoint_path,
        OUTPUT_TENSOR_NAME,
        'save/restore_all',
        'save/Const:0',
        os.path.join(EXPORT_FOLDER, 'fozen.pb'),
        True,
        ''
    )
    input_graph_def = tf.GraphDef()
    with tf.gfile.Open(os.path.join(EXPORT_FOLDER, 'fozen.pb'), "rb") as f:
        input_graph_def.ParseFromString(f.read())
    output_graph = optimize_for_inference(
        input_graph_def,
        [INPUT_TENSOR_NAME],
        [OUTPUT_TENSOR_NAME],
        tf.float32.as_datatype_enum
    )
    with tf.gfile.FastGFile(EXPORTED_MODEL_NAME, 'w') as f:
        f.write(output_graph.SerializeToString())

if __name__ == "__main__":
    export()
