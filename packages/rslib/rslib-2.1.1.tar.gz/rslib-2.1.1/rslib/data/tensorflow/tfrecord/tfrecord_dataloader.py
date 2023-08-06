#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
FeatureUtil

Authors: (zouzhene@corp.netease.com)
Phone: 13261632788
Date: 2020/06/02
"""
import numpy as np

import tensorflow as tf

import torch
from tensorflow.python.data.ops import dataset_ops
from torch._six import int_classes, string_classes, container_abcs
from torch.utils.data._utils.collate import np_str_obj_array_pattern, default_collate_err_msg_format

from rslib.utils.param_check import param_check


def read_tfrecord(filename, config, is_pred=False, batch_size=32, random_read=True):
    """
    加载 tfrecord 数据，并完成训练数据集的构造。
    包括序列特征构建、ID特征构建、稀疏特征构建、标签构建等

    Args:
        filename: 文件名；
        is_pred: 是否是预测阶段。

    Returns:
        TFRecordDataLoader
    """

    def _parse_exmp(serial_exmp):
        context_features = {
            "role_id_hash": tf.io.FixedLenFeature([], dtype=tf.int64),
            "cross_features_index": tf.io.VarLenFeature(dtype=tf.int64),
            "cross_features_val": tf.io.VarLenFeature(dtype=tf.float32),
            "user_features_id": tf.io.VarLenFeature(dtype=tf.int64),
            "cur_time": tf.io.FixedLenFeature([], dtype=tf.int64),
            "mask": tf.io.VarLenFeature(dtype=tf.int64),
            "label": tf.io.VarLenFeature(dtype=tf.int64),
        }

        for seq_num_i in range(config['seq_num']):
            context_features['sequence_id_' + str(seq_num_i)] = tf.io.VarLenFeature(dtype=tf.int64)
            context_features['sequence_time_' + str(seq_num_i)] = tf.io.VarLenFeature(dtype=tf.int64)
            context_features['sequence_time_gaps_' + str(seq_num_i)] = tf.io.VarLenFeature(dtype=tf.int64)

        context_parsed = tf.io.parse_single_example(serialized=serial_exmp, features=context_features)

        sequence_id = [tf.sparse_to_dense(context_parsed['sequence_id_' + str(i)].indices, [config['maxlen']],
                                          context_parsed['sequence_id_' + str(i)].values) for i in range(config['seq_num'])]
        sequence_time = [tf.sparse_to_dense(context_parsed['sequence_time_' + str(i)].indices, [config['maxlen']],
                                            context_parsed['sequence_time_' + str(i)].values) for i in range(config['seq_num'])]
        sequence_time_gaps = [tf.sparse_to_dense(context_parsed['sequence_time_gaps_' + str(i)].indices, [config['maxlen']],
                                                 context_parsed['sequence_time_gaps_' + str(i)].values)
                              for i in range(config['seq_num'])]
        role_id_hash = context_parsed['role_id_hash']
        cross_features_index = tf.sparse.to_dense(context_parsed['cross_features_index'])
        cross_features_val = tf.sparse.to_dense(context_parsed['cross_features_val'])
        cross_feature = tf.SparseTensor(values=cross_features_val, indices=tf.expand_dims(cross_features_index, -1),
                                        dense_shape=[config['cross_feature_num']])
        user_feature = tf.sparse.to_dense(context_parsed['user_features_id'])

        cur_time = context_parsed['cur_time']
        # mask = tf.sparse.to_dense(context_parsed['mask'])
        # label = tf.sparse.to_dense(context_parsed['label'])
        mask = tf.sparse.to_dense(context_parsed['mask'])
        label = tf.sparse.to_dense(context_parsed['label'])

        # 构建 mask 向量
        indices = tf.expand_dims(mask, -1)
        updates = tf.ones_like(mask)
        shape = tf.constant([config['output_unit']], dtype='int64')
        mask_tmp = tf.scatter_nd(indices, updates, shape)
        #
        # 构建 label 向量
        indices = tf.expand_dims(mask, -1)
        updates = label
        shape = tf.constant([config['output_unit']], dtype='int64')
        label_tmp = tf.scatter_nd(indices, updates, shape)

        mask, label = mask_tmp, label_tmp

        return role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_feature, user_feature, cur_time, mask, label

    def _flat_map_fn(role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_feature, user_feature, cur_time, mask, label):

        return dataset_ops.Dataset.zip((
            role_id_hash.batch(batch_size=batch_size),
            sequence_id.padded_batch(batch_size, padded_shapes=([config['seq_num'], config['maxlen']])),
            sequence_time.padded_batch(batch_size, padded_shapes=([config['seq_num'], config['maxlen']])),
            sequence_time_gaps.padded_batch(batch_size, padded_shapes=([config['seq_num'], config['maxlen']])),
            cross_feature.batch(batch_size=batch_size),
            user_feature.padded_batch(batch_size, padded_shapes=([config['user_feature_num']])),
            cur_time.batch(batch_size=batch_size),
            mask.batch(batch_size=batch_size),
            label.batch(batch_size=batch_size),
        ))

    def preprocess_fn(*args):
        """A transformation function to preprocess raw data
        into trainable input.
        """
        return args[:-1], args[-1]
        # return (a, b, c, d, e, f, g, i), tf.one_hot(h, config['output_unit']) if config['output_unit'] > 1 else h

    # tf.enable_eager_execution()
    dataset = tf.data.TFRecordDataset(filename, num_parallel_reads=4)
    if is_pred:
        dataset_train = dataset \
            .map(_parse_exmp, num_parallel_calls=1) \
            .window(size=batch_size, drop_remainder=False) \
            .flat_map(_flat_map_fn) \
            .map(preprocess_fn)
    else:
        dataset_train = dataset \
            .map(_parse_exmp, num_parallel_calls=4)
        if random_read:
            dataset_train = dataset_train.shuffle(100000)
        dataset_train = dataset_train.window(size=batch_size, drop_remainder=True) \
            .flat_map(_flat_map_fn) \
            .map(preprocess_fn) \
            .repeat()
    # print(dataset_train.make_one_shot_iterator().get_next())
    return dataset_train


def get_tfrecord_dataloader(file, config, batch_size=None, random_read=None):
    """Get the DataLoader used to read TFRecordDataset.

    With the Dataloader, you can read TFRecordDataset concurrently.
    Each time the iterator is requested to obtain a batch of training samples.

    Args:
        dataset (Dataset): dataset from which to load the data.
        batch_size (int, optional): how many samples per batch to load
            (default: ``1``).
        num_workers (int, optional): how many subprocesses to use for data
            loading. ``0`` means that the data will be loaded in the main process.
            (default: ``0``)
        pin_memory (bool, optional): If ``True``, the data loader will copy Tensors
            into CUDA pinned memory before returning them.  If your data elements
            are a custom type, or your :attr:`collate_fn` returns a batch that is a custom type,
            see the example below.

    Returns:
        a DataLoader
    """
    batch_size = param_check(config, 'batchsize', batch_size, 32)
    random_read = param_check(config, 'random_read', random_read, True)

    data_loader = read_tfrecord(file, config, batch_size=batch_size, random_read=random_read)

    return data_loader


if __name__ == '__main__':
    # done

    from demo.qier.code import param

    file = '/root/rslib/demo/qier/code/dataset/2019-11-21.age_trainset.tfrecord'

    config = param.config
    config['batchsize'] = 3

    random_read = False
    dataset_train = get_tfrecord_dataloader(file, config, random_read=random_read)
    xx = dataset_train.make_one_shot_iterator().get_next()
    with tf.Session() as sess:
        for _ in range(5):
            a = sess.run(xx)
            print(a[1])
