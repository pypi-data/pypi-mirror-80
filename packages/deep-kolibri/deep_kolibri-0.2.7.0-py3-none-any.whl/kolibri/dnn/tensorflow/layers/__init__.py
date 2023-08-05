
from tensorflow.python import keras

from kolibri.dnn.tensorflow.layers.att_wgt_avg_layer import AttentionWeightedAverage, AttWgtAvgLayer
from kolibri.dnn.tensorflow.layers .att_wgt_avg_layer import AttentionWeightedAverageLayer
from kolibri.dnn.tensorflow.layers.folding_layer import FoldingLayer
from kolibri.dnn.tensorflow.layers.kmax_pool_layer import KMaxPoolingLayer, KMaxPoolLayer, KMaxPooling
from kolibri.dnn.tensorflow.layers.non_masking_layer import NonMaskingLayer
from kapre.composed import get_melspectrogram_layer
from tensorflow.keras.layers import BatchNormalization
Melspectrogram= get_melspectrogram_layer

L = keras.layers

if __name__ == "__main__":
    print("Hello world")
