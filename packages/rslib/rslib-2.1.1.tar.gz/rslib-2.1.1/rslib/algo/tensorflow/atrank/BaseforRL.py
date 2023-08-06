import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.python import keras
from tensorflow.python.keras import layers, regularizers

from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K

from rslib.algo.tensorflow.layers.interaction import BiInteractionPooling
from .ATRankLayer import ATRankLayer, PositionalEncoding, BuySequence

from rslib.algo.tensorflow.utils import input_holder
from rslib.algo.tensorflow.utils.Input_processing import id_input_processing, cross_input_processing, sequence_embedding, sequence_group_embedding, sequence_tar_embedding
from rslib.algo.tensorflow.utils.model_compile import compile_model


def get_model(config, return_session=False, one_seq=False):
    '''
    get ATRank model
    https://arxiv.org/abs/1711.06632
    :param config:
    :return:
    '''
    activation = 'relu'
    hidden_unit = config['hidden_units']
    output_unit = config['output_unit']
    is_amp = config['is_amp']
    is_serving = config['is_serving']
    output_type = config['output_type']
    hidden_unit = config['hidden_units']
    class_num = config['class_num']
    emb_size = config['emb_size']
    maxlen = config['maxlen']

    l2 = 0
    dp = 0.1

    # todo，支持定制的输入格式
    input_list = []

    [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, cur_time_input, output_mask_input], model_input = input_holder.getInput(config, one_seq=one_seq)

    user_feature = id_input_processing(user_feature_input, config)
    user_feature = layers.Dropout(dp)(user_feature)
    user_feature = layers.Flatten()(user_feature)

    seq_index_layer = layers.Lambda(lambda x: x[0][:, x[1]])

    seq0 = seq_index_layer([sequence_id_input, 0])
    time0 = seq_index_layer([sequence_time_input, 0])
    layers_emb_sequence_feature0 = layers.Embedding(input_dim=class_num, output_dim=emb_size,
                                                    embeddings_regularizer=regularizers.l2(l2))
    seq0 = layers_emb_sequence_feature0(seq0)
    # seq0 = layers.Dense(hidden_unit, activation='relu', kernel_regularizer=regularizers.l2(l2))(seq0)
    seq0 = layers.Dropout(dp)(seq0)

    seq_con = layers.Lambda(lambda x: tf.tile(tf.constant(0, dtype=tf.int64, shape=(1, 1)), [tf.shape(sequence_time_input)[0], 1]))(1)
    seq_con = layers_emb_sequence_feature0(seq_con)
    # seq_con = layers.Dense(hidden_unit, activation='relu', kernel_regularizer=regularizers.l2(l2))(seq_con)
    time_con = layers.Lambda(lambda x: tf.tile(tf.constant(1, dtype=tf.int64, shape=(1, 1)), [tf.shape(sequence_time_input)[0], 1]))(1)

    att = ATRankLayer(config=config, type='encode', name='xx0')([seq0, seq_con], mask=[time0, time_con], learning_phase=K.learning_phase())
    seq0_mean = layers.Lambda(lambda x: x[:, 0])(att)

    seq0_mean = layers.Concatenate(axis=1)([user_feature, seq0_mean])
    if not one_seq:
        seq2 = seq_index_layer([sequence_id_input, 2])
        seq3 = seq_index_layer([sequence_id_input, 3])
        time2 = seq_index_layer([sequence_time_input, 2])
        time3 = seq_index_layer([sequence_time_input, 3])

        seq3, time3, seq4, time4 = BuySequence(config=config)([seq3, time3])

        layers_emb_sequence_feature2 = layers.Embedding(input_dim=class_num, output_dim=emb_size,
                                                        embeddings_regularizer=regularizers.l2(l2))
        layers_emb_sequence_feature3 = layers.Embedding(input_dim=class_num, output_dim=emb_size,
                                                        embeddings_regularizer=regularizers.l2(l2))
        layers_emb_sequence_feature4 = layers.Embedding(input_dim=class_num, output_dim=emb_size,
                                                        embeddings_regularizer=regularizers.l2(l2))

        seq2 = layers_emb_sequence_feature2(seq2)
        seq3 = layers_emb_sequence_feature3(seq3)
        seq4 = layers_emb_sequence_feature4(seq4)


        seq2 = layers.Concatenate(axis=2)([seq2,
                                           tf.tile(seq0_mean[:, tf.newaxis], [1, maxlen, 1]),
                                           ])
        seq2 = layers.Dense(hidden_unit, activation='relu',
                            kernel_regularizer=regularizers.l2(l2))(seq2)
        seq2 = layers.Dropout(dp)(seq2)
        # seq2 = layers.Dense(hidden_unit, activation='sigmoid')(seq2)
        seq3 = layers.Concatenate(axis=2)([seq3,
                                           tf.tile(seq0_mean[:, tf.newaxis], [1, maxlen, 1]),
                                           ])
        seq3 = layers.Dense(hidden_unit, activation='relu',
                            kernel_regularizer=regularizers.l2(l2))(seq3)
        seq3 = layers.Dropout(dp)(seq3)
        # seq3 = layers.Dense(hidden_unit, activation='sigmoid')(seq3)
        seq4 = layers.Concatenate(axis=2)([seq4,
                                           tf.tile(seq0_mean[:, tf.newaxis], [1, 1, 1]),
                                           ])
        seq4 = layers.Dense(hidden_unit, activation='relu',
                            kernel_regularizer=regularizers.l2(l2))(seq4)
        seq4 = layers.Dropout(dp)(seq4)

        seq_con = layers.Lambda(lambda x: tf.tile(tf.constant(0, dtype=tf.int64, shape=(1, 1)), [tf.shape(sequence_time_input)[0], 1]))(1)
        seq_con = layers_emb_sequence_feature2(seq_con)
        # seq_con = layers.Dense(hidden_unit, activation='relu', kernel_regularizer=regularizers.l2(l2))(seq_con)
        time_con = layers.Lambda(lambda x: tf.tile(tf.constant(1, dtype=tf.int64, shape=(1, 1)), [tf.shape(sequence_time_input)[0], 1]))(1)
        seq_2 = ATRankLayer(config=config, type='encode', name='xx2')([seq2, seq_con], mask=[time2, time_con], learning_phase=K.learning_phase())

        seq_con = layers.Lambda(lambda x: tf.tile(tf.constant(0, dtype=tf.int64, shape=(1, 1)), [tf.shape(sequence_time_input)[0], 1]))(1)
        seq_con = layers_emb_sequence_feature3(seq_con)
        # seq_con = layers.Dense(hidden_unit, activation='relu', kernel_regularizer=regularizers.l2(l2))(seq_con)
        time_con = layers.Lambda(lambda x: tf.tile(tf.constant(1, dtype=tf.int64, shape=(1, 1)), [tf.shape(sequence_time_input)[0], 1]))(1)
        seq_3 = ATRankLayer(config=config, type='encode', name='xx3')([seq3, seq_con], mask=[time3, time_con], learning_phase=K.learning_phase())

        seq_con = layers.Lambda(lambda x: tf.tile(tf.constant(0, dtype=tf.int64, shape=(1, 1)), [tf.shape(sequence_time_input)[0], 1]))(1)
        seq_con = layers_emb_sequence_feature4(seq_con)
        # seq_con = layers.Dense(hidden_unit, activation='relu', kernel_regularizer=regularizers.l2(l2))(seq_con)
        time_con = layers.Lambda(lambda x: tf.tile(tf.constant(1, dtype=tf.int64, shape=(1, 1)), [tf.shape(sequence_time_input)[0], 1]))(1)
        seq_4 = ATRankLayer(config=config, type='encode', name='xx4')([seq4, seq_con], mask=[time4, time_con], learning_phase=K.learning_phase())

        seq_2 = layers.Lambda(lambda x: x[:, 0])(seq_2)
        seq_3 = layers.Lambda(lambda x: x[:, 0])(seq_3)
        seq_4 = layers.Lambda(lambda x: x[:, 0])(seq_4)

        # seq_2_lstm = layers.LSTM(units=hidden_unit)(seq2)
        # seq_3_lstm = layers.LSTM(units=hidden_unit)(seq3)
        # seq_4_lstm = layers.LSTM(units=hidden_unit)(seq4)

        # att = ATRankLayer(config=config, type='encode', name='xx3')([seq_concat, seq_concat], mask=[time_concat, time_concat], learning_phase=K.learning_phase())
        # att_all_seq4 = ATRankLayer(config=config, type='encode', name='yy')([att, seq4], mask=[time_concat, time4], learning_phase=K.learning_phase())
        # all_feature = layers.Lambda(lambda x: x[:, 0])(att_all_seq4)

        all_feature = layers.Concatenate(axis=1)([seq_2, seq_3, seq_4])

        all_feature = layers.Dense(hidden_unit, activation='relu',
                                   kernel_regularizer=regularizers.l2(l2))(all_feature)

        all_feature = layers.Dropout(dp)(all_feature)

        output = layers.Dense(output_unit,
                              kernel_regularizer=regularizers.l2(l2))(all_feature)

        output_layer = {
            'multi_class': tf.nn.softmax,
            'multi_label': tf.sigmoid,
            'regression': lambda x: x,
            'multi_regression': lambda x: x
        }[output_type]
        # output_layer = layers.Activation('softmax')
        output = output
        output = output_layer(output)
    if one_seq:
        model = Model(inputs=model_input, outputs=[seq0_mean])
    else:
        model = Model(inputs=model_input, outputs=[output])
    model, sess = compile_model(model, config)

    print(model.summary())
    if return_session:
        return model, sess
    else:
        return model
