import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import time

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
saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)
saver.restore(sess, "./para")