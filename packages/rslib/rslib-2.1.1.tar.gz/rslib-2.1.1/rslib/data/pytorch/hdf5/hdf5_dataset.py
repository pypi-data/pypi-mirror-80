#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
hdf5 Dataset

Authors: (zouzhene@corp.netease.com)
Phone: 13261632788
Date: 2020/06/02
"""
import math
import torch
import h5py
import numpy as np


def worker_init_fn(worker_id):
    '''
    并发加载 HDF5Dataset 时，为每个进程指定不同的 HDF5Dataset_chunk。
    每个进程获得的 HDF5Dataset_chunk 是随机的。
    :param worker_id:
    :return:
    '''
    from numpy import random
    worker_info = torch.utils.data.get_worker_info()
    works_num = worker_info.num_workers
    dataset = worker_info.dataset
    worker_id = worker_info.id
    seed = worker_info.seed % 10000
    length = dataset.length
    random_read = dataset.random_read

    #   数据分chunk
    chunk_num = int(math.ceil(length / float(dataset.chunk_size)))
    random_chunk_ids = np.arange(chunk_num)
    random.seed(seed - worker_id)
    if random_read:
        np.random.shuffle(random_chunk_ids)
    random.seed(seed)
    #     print(random_chunk_ids)

    #  chunk分work
    works_size = int(math.ceil(chunk_num / works_num))
    worker_id = worker_info.id
    start_i = works_size * worker_id
    end_i = min(works_size * (worker_id + 1), chunk_num)
    dataset.chunk_ids = random_chunk_ids[start_i: end_i]
    dataset.datasets = [dataset.new_chunk(dataset.file_path, chunk_id, dataset.chunk_size, dataset.length) for chunk_id in dataset.chunk_ids]


class HDF5Dataset_chunk(torch.utils.data.IterableDataset):
    '''
        用于读取 hdf5 文件片段的 Dataset。该Dataset对数据的读取是乱序的。
        :param file_path: file_path
        :param chunk_id: 片段ID
        :param chunk_size: 片段最多包含的数据量
        :param length: 片段实际包含的数据量
        :param colum_name: 需要读取的列
        '''

    def __init__(self, file_path, chunk_id, chunk_size, length, colum_name, random_read):

        super(HDF5Dataset_chunk).__init__()

        self.file_path = file_path
        self.chunk_id = chunk_id
        self.chunk_size = chunk_size

        self.start = self.chunk_size * self.chunk_id
        self.end = min(self.chunk_size * (self.chunk_id + 1), length)
        self.length = self.end - self.start
        self.data = None

        self.colum_name = colum_name
        self.random_read = random_read

    def __iter__(self):
        if self.data is None:
            self.data = h5py.File(self.file_path, 'r')

        order = np.arange(self.length)
        if self.random_read:
            np.random.shuffle(order)
        #         print(self.start, self.end)

        if self.colum_name is None:
            colum_name = ['role_id_hash', 'sequence_id', 'sequence_time', 'sequence_time_gaps', 'cross_features_index',
                          'cross_features_val', 'user_features_id', 'cur_time', 'mask', 'label']
        else:
            colum_name = self.colum_name

        data = [self.data[n][self.start: self.end] for n in colum_name]
        return iter([d[x] if i != len(data) - 1 else d[x] for i, d in enumerate(data)] for x in order)
        # return iter(([d[x] for d in data[:-1]], data[-1][x][0]) for x in order)

    def __len__(self):
        return self.length


class HDF5Dataset(torch.utils.data.IterableDataset):
    """用于并发读取的 HDF5Dataset。HDF5Dataset 由若干 HDF5Dataset_chunk 组成，每个 HDF5Dataset_chunk 用于读取 hdf5 中某个片段的数据,
    不同 HDF5Dataset_chunk 间读取数据是并发的

    Args:
        hdf5_path: hdf5_path
        chunk_size: 每个 HDF5Dataset_chunk 包含的数据量
        colum_name: 读取哪几列数据

    """

    def __init__(self, file_path, chunk_size, colum_name, random_read):

        super(HDF5Dataset).__init__()
        self.file_path = file_path
        self.first = True
        self.data = None
        with h5py.File(self.file_path, 'r') as file:
            self.length = len(file['label'])

        self.chunk_size = chunk_size
        self.chunk_ids = None
        self.datasets = None

        self.colum_name = colum_name
        self.random_read = random_read

    def __iter__(self):
        for d in self.datasets:
            assert isinstance(d, torch.utils.data.IterableDataset), "ChainDataset only supports IterableDataset"
            for x in d:
                yield x

    def __len__(self):
        return self.length

    def new_chunk(self, file_path, chunk_id, chunk_size, length):
        return HDF5Dataset_chunk(file_path, chunk_id, chunk_size, length, self.colum_name, self.random_read)


def get_hdf5_dataset(hdf5_path, chunk_size, colum_name=None, random_read=True):
    """Get a HDF5Dataset.

    HDF5Dataset: HDF5Dataset is composed of several HDF5Dataset_chunk, each HDF5Dataset_chunk is used to read the data of a fragment in hdf5,
    Reading data between different HDF5Dataset_chunk is concurrent.

    Args:
        hdf5_path (str): The path to the hdf5 file.
        chunk_size (int): chunk size.
        colum_name (list): List or dict of str, optional, default=None
            List of keys or dict of (key, value) pairs to extract from each
            record. The keys represent the name of the features and the
            values ("byte", "float", or "int") correspond to the data type.
            If dtypes are provided, then they are verified against the
            inferred type for compatibility purposes. If None (default),
            then all features contained in the file are extracted.

    Returns:
        a HDF5Dataset.
    """
    dataset = HDF5Dataset(hdf5_path, chunk_size, colum_name, random_read)
    return dataset
