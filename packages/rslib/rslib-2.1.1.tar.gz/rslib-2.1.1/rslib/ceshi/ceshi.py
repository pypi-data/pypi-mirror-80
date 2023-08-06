from tensorflow.python.keras.layers import Dense, Input
from tensorflow.python.keras.models import Model
import scipy
import numpy as np
import tensorflow as tf

from rslib.algo.tensorflow.sparse_dnn.DenseLayerForSparse import DenseLayerForSparse
import numpy as np
from scipy.sparse import csr_matrix,coo_matrix

row = np.array([0, 0, 1, 2, 2, 2])
col = np.array([0, 2, 2, 0, 1, 2])
data = np.array([1, 2, 3, 4, 5, 6])
trainX = coo_matrix((data, (row, col)), shape=(3, 3))

trainY = np.random.rand(3, 3)

inputs = Input(shape=(3,), sparse=True)
cross_feature = DenseLayerForSparse(10, 3, 'relu')(inputs)
# cross_feature = tf.ones_like(inputs, dtype=tf.float32)
model = Model(inputs=inputs, outputs=cross_feature)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

steps = 10
for i in range(steps):
    # For simplicity, we directly use trainX and trainY in this example
    # Usually, this is where batches are prepared
    # print(model.fit(trainX, trainY))
    print(model.train_on_batch(trainX, trainY))
