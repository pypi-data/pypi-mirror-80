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
import collections
import time

import math
import random

import h5py
import numpy as np
import tensorflow as tf
from tensorflow.contrib import eager
from tensorflow.python.data.ops import dataset_ops

import param
from rslib.core.FeatureUtil import FeatureUtil
from rslib.data.util.hdf5_generator import HDF5Generator
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
    cross_type = config['cross_type']

    def _parse_exmp(role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_features_index, cross_features_val, user_features_id, cur_time, mask, label):
        cross_feature = tf.SparseTensor(values=cross_features_val, indices=tf.expand_dims(cross_features_index, -1),
                                        dense_shape=[config['cross_feature_num']])

        return role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_feature, user_features_id, cur_time, mask, label

    # def _flat_map_fn(role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_features_index, cross_features_val, user_features_id, cur_time, pos_label):
    def _flat_map_fn(role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_features, user_features_id, cur_time, mask, label):
        return dataset_ops.Dataset.zip((
            role_id_hash.batch(batch_size=batch_size),
            sequence_id.batch(batch_size=batch_size),
            sequence_time.batch(batch_size=batch_size),
            sequence_time_gaps.batch(batch_size=batch_size),
            cross_features.batch(batch_size=batch_size),
            user_features_id.batch(batch_size=batch_size),
            cur_time.batch(batch_size=batch_size),
            mask.batch(batch_size=batch_size),
            label.batch(batch_size=batch_size),
        ))

    def preprocess_fn(*args):
        """A transformation function to preprocess raw data
        into trainable input.
        """
        return args[:-1], args[-1]

    # def preprocess_fn(a, b, c, d, e, f, g, h, i):
    #     """A transformation function to preprocess raw data
    #     into trainable input.
    #     """
    #     return (a, b, c, d, e, f, g, h), i

    label_type = tf.float32 if 'regression' in config['output_type'] else tf.int64
    dataset = tf.data.Dataset.from_generator(
        HDF5Generator(filename, random_read=False),
        (tf.int64, tf.int64, tf.int64, tf.int64, tf.int64, tf.float32, tf.int64, tf.int64, tf.int64, label_type),
        (tf.TensorShape([]), tf.TensorShape([None, None]), tf.TensorShape([None, None]), tf.TensorShape([None, None]), tf.TensorShape([None]),
         tf.TensorShape([None]), tf.TensorShape([None]), tf.TensorShape([]), tf.TensorShape([None]), tf.TensorShape([None]))
    )

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
            dataset_train = dataset_train.shuffle(10000)
        dataset_train = dataset_train.window(size=batch_size, drop_remainder=True) \
            .flat_map(_flat_map_fn) \
            .map(preprocess_fn) \
            .repeat()

    return dataset_train


def get_hdf5_dataloader(file, config, batch_size=None, random_read=None):
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
    eager.enable_eager_execution()
    file = '/root/rslib/demo/qier/code/dataset/2019-11-21.age_trainset.h5'
    config = {'batchsize': 3, 'cross_type': 'sparse1', 'output_type': 'regression', 'cross_feature_num': 10}
    dataset = get_hdf5_dataloader(file, config, random_read=False)

    print(11)
    it = dataset.make_one_shot_iterator()

    for _ in range(3):
        x = it.get_next()
        print(x[1])
