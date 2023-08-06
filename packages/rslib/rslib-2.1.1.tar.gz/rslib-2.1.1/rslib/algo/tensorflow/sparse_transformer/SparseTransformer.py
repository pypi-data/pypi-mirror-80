#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
keras_sparsetransformer

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/9/11
"""

import tensorflow as tf
from tensorflow.python.keras import layers
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K

from .SparseTransformerLayer import SparseTransformerLayer
from rslib.algo.tensorflow.utils import input_holder
from rslib.algo.tensorflow.utils.Input_processing import id_input_processing, cross_input_processing, sequence_embedding, sequence_group_embedding, sequence_tar_embedding
from rslib.algo.tensorflow.utils.model_compile import compile_model


def get_model(config):
    class_num = config['class_num']
    emb_size = config['sptransformer_emb_size']
    output_unit = config['output_unit']
    is_amp = config['is_amp']
    is_serving = config['is_serving']
    output_type = config['output_type']

    # todo，支持定制的输入格式
    input_list = []

    [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, cur_time_input, output_mask_input], model_input = input_holder.getInput(config)

    user_feature = id_input_processing(user_feature_input, config)
    cross_feature = cross_input_processing(cross_feature_input, config)

    seq_index_layer = layers.Lambda(lambda x: x[0][:, x[1]])
    seq_id = seq_index_layer([sequence_id_input, 0])
    seq_time = seq_index_layer([sequence_time_input, 0])
    seq_time_gaps = seq_index_layer([sequence_time_gaps_input, 0])
    seq_id_embeddings = layers.Embedding(class_num, emb_size, mask_zero=True)(seq_id)

    temp_input = seq_id_embeddings, seq_time
    transformer_enc = SparseTransformerLayer(config)(temp_input)
    all_feature = layers.Concatenate(axis=-1)([transformer_enc, user_feature, cross_feature])
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
    model = compile_model(model, config)

    print(model.summary())
    return model
