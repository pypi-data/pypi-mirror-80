#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
keras_han

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/9/11
"""

import tensorflow as tf
import sys
from tensorflow.python.keras import layers, regularizers
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K

from rslib.algo.tensorflow.attention.AttentionLayer import AttentionLayer, AttentionLayer2
from rslib.algo.tensorflow.layers.interaction import BiInteractionPooling
from rslib.algo.tensorflow.sparse_dnn.DenseLayerForSparse import DenseLayerForSparse
from rslib.algo.tensorflow.utils import input_holder
from rslib.algo.tensorflow.utils.model_compile import compile_model


def get_model(config, return_session=False, no_cross=False):
    activation = 'relu'
    hidden_unit = config['hidden_units']
    output_unit = config['output_unit']
    is_amp = config['is_amp']
    is_serving = config['is_serving']
    output_type = config['output_type']

    maxlen = config['maxlen']
    class_num = config['class_num']
    emb_size = config['emb_size']
    cross_feature_num = config['cross_feature_num']
    user_feature_num = config['user_feature_num']
    user_feature_size = config['user_feature_size']
    output_unit = config['output_unit']


    [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input,
     user_feature_input, output_mask_input, cur_time_input], model_input = input_holder.getInput(config)

    seq_index_layer = layers.Lambda(lambda x: x[0][:, :, x[1]])
    seq_time = seq_index_layer([sequence_time_input, 0])

    layers_emb_user_id = layers.Embedding(class_num, emb_size, input_length=maxlen, trainable=True, mask_zero=True)(sequence_id_input)

    review_encoder = layers.TimeDistributed(AttentionLayer2(config))(layers_emb_user_id)

    seqs_embeddings = AttentionLayer(config)([review_encoder, seq_time, seq_time])

    cross_feature = DenseLayerForSparse(cross_feature_num, hidden_unit, activation)(cross_feature_input)
    # cross_feature = layers.Lambda(lambda x: tf.ones([tf.shape(seq_id_input)[0], 128]))(1)

    layers_emb_fm1_user_feature = layers.Embedding(input_dim=user_feature_size, output_dim=1)
    layers_emb_fm2_user_feature = layers.Embedding(input_dim=user_feature_size, output_dim=emb_size)
    layers_FM = BiInteractionPooling()
    user_feature_1 = layers.Flatten()(layers_emb_fm1_user_feature(user_feature_input))
    user_feature_2 = layers.Flatten()(layers_FM(layers_emb_fm2_user_feature(user_feature_input)))
    user_feature = layers.Concatenate(axis=1)([user_feature_1, user_feature_2])

    if no_cross:
        all_feature = layers.Concatenate(axis=-1)([seqs_embeddings, user_feature])
    else:
        all_feature = layers.Concatenate(axis=-1)([seqs_embeddings, cross_feature, user_feature])

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
    if return_session:
        return model, sess
    else:
        return model