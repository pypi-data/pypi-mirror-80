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
import torch

from torch._six import int_classes, string_classes, container_abcs
from torch.utils.data._utils.collate import np_str_obj_array_pattern, default_collate_err_msg_format

from rslib.data.pytorch.tfrecord.tfrecord_dataset import get_tfrecord_dataset
from rslib.utils.param_check import param_check


def rslib_collate(batch):
    """rslib 专用的 batching 方法，能够将 DataLoader 获取的多条数据处理成一个batch的样本, 包括：

     -  数据转换为 Tensor

     -  数据存入 shared 缓存

     -  稀疏向量处理

    Args:
        batch: DataLoader 获取的多条数据

    Returns:
        一个batch的样本
    """
    elem = batch[0]
    elem_type = type(elem)
    if isinstance(elem, torch.Tensor):
        out = None
        if torch.utils.data.get_worker_info() is not None:
            # If we're in a background process, concatenate directly into a
            # shared memory tensor to avoid an extra copy
            numel = sum([x.numel() for x in batch])
            storage = elem.storage()._new_shared(numel)
            out = elem.new(storage)
        return torch.stack(batch, 0, out=out)
    elif elem_type.__module__ == 'numpy' and elem_type.__name__ != 'str_' \
            and elem_type.__name__ != 'string_':
        elem = batch[0]
        if elem_type.__name__ == 'ndarray':
            # array of string classes and object
            if np_str_obj_array_pattern.search(elem.dtype.str) is not None:
                raise TypeError(default_collate_err_msg_format.format(elem.dtype))

            return rslib_collate([torch.as_tensor(b) for b in batch])
        elif elem.shape == ():  # scalars
            return torch.as_tensor(batch)
    elif isinstance(elem, float):
        return torch.tensor(batch, dtype=torch.float64)
    elif isinstance(elem, int_classes):
        return torch.tensor(batch)
    elif isinstance(elem, string_classes):
        return batch
    elif isinstance(elem, container_abcs.Mapping):
        return {key: rslib_collate([d[key] for d in batch]) for key in elem}
    elif isinstance(elem, tuple) and hasattr(elem, '_fields'):  # namedtuple
        return elem_type(*(rslib_collate(samples) for samples in zip(*batch)))
    elif isinstance(elem, container_abcs.Sequence):
        transposed = zip(*batch)
        res1 = []
        res1.append(rslib_collate(transposed.__next__()))
        res1.append(rslib_collate(transposed.__next__()))
        res1.append(rslib_collate(transposed.__next__()))
        res1.append(rslib_collate(transposed.__next__()))

        indice = transposed.__next__()
        indice2 = torch.LongTensor([[i, y] for i, x in enumerate(indice) for y in x]).share_memory_()
        res1.append(indice2)
        value = transposed.__next__()
        value2 = torch.FloatTensor([y for x in value for y in x]).share_memory_()
        res1.append(value2)

        res1.append(rslib_collate(transposed.__next__()))
        res1.append(rslib_collate(transposed.__next__()))
        res1.append(rslib_collate(transposed.__next__()))

        res2 = rslib_collate(transposed.__next__())
        return res1, res2

    raise TypeError(default_collate_err_msg_format.format(elem_type))


def get_tfrecord_dataloader(file, config, batch_size=None, random_read=None, pin_memory=True):
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

    dataset = get_tfrecord_dataset(file, config, random_read)
    num_workers = 1
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, num_workers=num_workers,
                                              collate_fn=rslib_collate,
                                              pin_memory=pin_memory)
    return data_loader


if __name__ == '__main__':
    # done

    from demo.qier.code import param

    config = param.config

    file = '/root/rslib/demo/qier/code/dataset/2019-11-21.age_trainset.tfrecord'

    random_read = True
    dataloader = get_tfrecord_dataloader(file, config, batch_size=3, random_read=random_read)

    for i in dataloader:
        i
        print(len(i))
        print(i[1])
