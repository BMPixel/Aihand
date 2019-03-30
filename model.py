import warnings
warnings.filterwarnings('ignore')
from sys import stdout
stdout.flush()
print("MSGLoadingHeader")
stdout.flush()
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import time

stdout.flush()
print("MSGBuildGraph")
stdout.flush()
batch_size = 56
tf.reset_default_graph()

Wh = tf.Variable(tf.random_normal([8, 32]))
bh = tf.Variable(tf.random_normal([32]))
Wo = tf.Variable(tf.random_normal([32, 1]))
bo = tf.Variable(tf.random_normal([1]))

lstm_cell = tf.nn.rnn_cell.LSTMCell(32, forget_bias=0, state_is_tuple=True)
train_init = lstm_cell.zero_state(batch_size, "float")
a = tf.placeholder("float", [None, 96, 32])

outputs, state = tf.nn.dynamic_rnn(lstm_cell, a, initial_state=train_init)
sess = tf.Session()
# saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)
saver = tf.train.Saver()
saver.restore(sess, "/home/pi/Desktop/Workspace/para")

_s = tf.nn.rnn_cell.LSTMStateTuple(tf.placeholder("float",[1, 32]), tf.placeholder("float", [1, 32]))
_o = tf.placeholder("float", [1, 32])
_x = tf.placeholder("float", [1, 8])
_a = tf.nn.softsign(tf.matmul(_x, Wh) + bh)
_cell = lstm_cell(inputs=_a, state=_s)
_y = tf.sigmoid(tf.matmul(_o, Wo) + bo)
hist = []

feed_state = (np.zeros((1, 32)), np.zeros((1, 32)))
def run(arr):
    global feed_state
    feed_out, feed_state = sess.run(
        _cell, feed_dict={
            _x: arr,
            _s: feed_state
        })

    ans = sess.run(_y, feed_dict={_o: feed_out})
    return ans