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
import typing
import numpy as np

import torch.utils.data

from rslib.data.pytorch.tfrecord.util import reader, iterator_utils




class TFRecordDataset(torch.utils.data.IterableDataset):
    """Parse (generic) TFRecords dataset into `IterableDataset` object,
    which contain `np.ndarrays`s.

    Args:
        data_path: str
            The path to the tfrecords file.
        index_path: str or None
            The path to the index file.
        description: list or dict of str, optional, default=None
            List of keys or dict of (key, value) pairs to extract from each
            record. The keys represent the name of the features and the
            values ("byte", "float", or "int") correspond to the data type.
            If dtypes are provided, then they are verified against the
            inferred type for compatibility purposes. If None (default),
            then all features contained in the file are extracted.
        shuffle_queue_size: int, optional, default=None
            Length of buffer. Determines how many records are queued to
            sample from.
        transform : a callable, default = None
            A function that takes in the input `features` i.e the dict
            provided in the description, transforms it and returns a
            desirable output.

    """

    def __init__(self,
                 data_path: str,
                 index_path: typing.Union[str, None],
                 description: typing.Union[typing.List[str], typing.Dict[str, str], None] = None,
                 shuffle_queue_size: typing.Optional[int] = None,
                 transform: typing.Callable[[dict], typing.Any] = None
                 ) -> None:
        super(TFRecordDataset, self).__init__()
        self.data_path = data_path
        self.index_path = index_path
        self.description = description
        self.shuffle_queue_size = shuffle_queue_size
        self.transform = transform or (lambda x: x)

    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is not None:
            shard = worker_info.id, worker_info.num_workers
            np.random.seed(worker_info.seed % np.iinfo(np.uint32).max)
        else:
            shard = None
        it = reader.tfrecord_loader(
            self.data_path, self.index_path, self.description, shard)
        if self.shuffle_queue_size:
            it = iterator_utils.shuffle_iterator(it, self.shuffle_queue_size)
        if self.transform:
            it = map(self.transform, it)
        return it


def get_tfrecord_dataset(tfrecord_path, config, random_read=True, description=None, transform=None):
    """Get a TFRecordDataset.

    TFRecordDataset: Parse (generic) TFRecords dataset into `IterableDataset` object, which contain `np.ndarrays`s.

    Args:
        tfrecord_path (str): The path to the tfrecords file.
        description: list or dict of str, optional, default=None
            List of keys or dict of (key, value) pairs to extract from each
            record. The keys represent the name of the features and the
            values ("byte", "float", or "int") correspond to the data type.
            If dtypes are provided, then they are verified against the
            inferred type for compatibility purposes. If None (default),
            then all features contained in the file are extracted.
        shuffle_queue_size: int, optional, default=None
            Length of buffer. Determines how many records are queued to
            sample from.

        transform : a callable, default = None
            A function that takes in the input `features` i.e the dict
            provided in the description, transforms it and returns a
            desirable output.

    Returns:
        a TFRecordDataset
    """
    index_path = None
    if description is None:
        description = {
            "role_id_hash": "int",
            "cross_features_index": "int",
            "cross_features_val": "float",
            "user_features_id": "int",
            "cur_time": "int",
            'mask': "int",
            "label": "int",
        }
        for i in range(config['seq_num']):
            description["sequence_id_" + str(i)] = 'int'
            description["sequence_time_" + str(i)] = 'int'
            description["sequence_time_gaps_" + str(i)] = 'int'

    if transform is None:
        def decode_feature(features):
            sequence_id = []
            sequence_time = []
            sequence_time_gaps = []
            maxlen = config['maxlen']
            for i in range(config['seq_num']):
                sequence_id.append(np.pad(features["sequence_id_" + str(i)], (0, maxlen - len(features["sequence_id_" + str(i)])), 'constant', constant_values=(0, 0)).astype(np.int64))
                sequence_time.append(np.pad(features["sequence_time_" + str(i)], (0, maxlen - len(features["sequence_time_" + str(i)])), 'constant', constant_values=(0, 0)).astype(np.int64))
                sequence_time_gaps.append(np.pad(features["sequence_time_gaps_" + str(i)], (0, maxlen - len(features["sequence_time_gaps_" + str(i)])), 'constant', constant_values=(0, 0)).astype(np.int64))
            sequence_id = np.array(sequence_id)
            sequence_time = np.array(sequence_time)
            sequence_time_gaps = np.array(sequence_time_gaps)

            role_id_hash = features['role_id_hash'].astype(np.int64)[0]
            cross_features_index = features['cross_features_index'].astype(np.int64)
            cross_features_val = features['cross_features_val'].astype(np.float32)

            user_features_id = features['user_features_id'].astype(np.int64)
            cur_time = features['cur_time'].astype(np.int64)[0]

            mask = features['mask'].astype(np.int64)
            label = features['label'].astype(np.int64)
            mask_tmp = [0] * config['output_unit']
            label_tmp = [0] * config['output_unit']

            for item_mask, item_label in zip(mask, label):
                mask_tmp[item_mask] = 1
                label_tmp[item_mask] = item_label

            mask, label = np.array(mask_tmp, dtype=np.int64), np.array(label_tmp, dtype=np.int64)

            return [role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_features_index, cross_features_val,
                    user_features_id, cur_time, mask, label]

        transform = decode_feature

    shuffle_queue_size = 10000 if random_read else None
    print(shuffle_queue_size)
    dataset = TFRecordDataset(tfrecord_path, index_path, description, transform=transform, shuffle_queue_size=shuffle_queue_size)
    return dataset
