#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
keras_lstm

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/9/11
"""

import collections
import tensorflow as tf

from tensorflow.python.keras import layers, regularizers
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K

from rslib.algo.tensorflow.utils import input_holder
from rslib.algo.tensorflow.utils.Input_processing import id_input_processing, cross_input_processing, sequence_input_LSTM
from rslib.algo.tensorflow.utils.model_compile import compile_model


def get_model(config):
    output_unit = config['output_unit']
    is_amp = config['is_amp']
    is_serving = config['is_serving']
    output_type = config['output_type']

    # todo，支持定制的输入格式
    input_list = []

    [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, cur_time_input, output_mask_input], model_input = input_holder.getInput(config)

    user_feature = id_input_processing(user_feature_input, config)
    cross_feature = cross_input_processing(cross_feature_input, config)
    sequence_feature = sequence_input_LSTM(sequence_id_input, config)

    all_feature = layers.Concatenate(axis=-1)([sequence_feature, cross_feature, user_feature])
    output = layers.Dense(output_unit)(all_feature)

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
    model, sess = compile_model(model, config)

    print(model.summary())
    return model, sess
