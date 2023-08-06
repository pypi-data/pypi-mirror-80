import os
import json
import numpy as np
import tensorflow as tf

from tensorflow.python import keras
from tensorflow.python.keras import layers, regularizers

from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K

from .DINLayer import DINLayer

from rslib.algo.tensorflow.utils import input_holder
from rslib.algo.tensorflow.utils.Input_processing import id_input_processing, cross_input_processing, sequence_embedding, sequence_group_embedding, sequence_tar_embedding
from rslib.algo.tensorflow.utils.model_compile import compile_model


def get_model(config):
    '''

    :param config:
    :return:
    '''
    output_unit = config['output_unit']
    is_serving = config['is_serving']
    output_type = config['output_type']
    hidden_units = config['hidden_units']

    # todo，支持定制的输入格式
    input_list = []

    [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, cur_time_input, output_mask_input], model_input = input_holder.getInput(config)

    user_feature = id_input_processing(user_feature_input, config)
    cross_feature = cross_input_processing(cross_feature_input, config)

    dense_all, time_mask_all,_ = sequence_embedding(sequence_id_input, sequence_time_input, config)
    dense_group_target, time_mask_group_target = sequence_tar_embedding(sequence_id_input, sequence_time_input, config)

    seq_embedding = DINLayer(config=config)(dense_group_target, dense_all, mask=time_mask_all)

    output = layers.Concatenate(axis=-1)([seq_embedding, cross_feature, user_feature, layers.Flatten()(dense_group_target)])
    output = layers.Dense(hidden_units, activation='relu')(output)
    output = layers.Dense(hidden_units, activation='relu')(output)
    output = layers.Dense(output_unit)(output)

    if not is_serving:
        if output_type in ['multi_class', 'multi_label']:
            paddings = tf.ones_like(output) * (-2 ** 32 + 1)
            output = tf.where(tf.equal(output_mask_input, 0), paddings, output)
        elif output_type in ['regression', 'multi_regression']:
            paddings = tf.zeros_like(output)
            output = tf.where(tf.equal(output_mask_input, 0), paddings, output)

    output_layer = {
        'multi_class': tf.nn.softmax,
        'multi_label': tf.sigmoid,
        'regression': lambda x: x,
        'multi_regression': lambda x: x
    }[output_type]
    output = output_layer(output)
    model = Model(inputs=model_input, outputs=[output])
    model = compile_model(model, config)

    print(model.summary())
    return model
