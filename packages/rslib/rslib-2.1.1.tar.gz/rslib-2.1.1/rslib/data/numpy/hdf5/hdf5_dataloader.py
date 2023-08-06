import math

import numpy as np
from scipy.sparse import coo_matrix

from rslib.data.util.hdf5_generator import HDF5Generator
from rslib.utils.param_check import param_check


class HDF5toNumpy(object):
    def __init__(self, generator):
        self.generator = generator
        self.length = generator.length

    def batching(self, batch_size=1, format='col', cross_type='sparse'):
        generator = self.generator()
        length = self.length

        batch_num = int(math.ceil(length / batch_size))

        for i in range(batch_num):
            batch = []
            for j in range(batch_size):
                if i * batch_size + j == length:
                    break
                data = generator.__next__()
                batch.append(data)
            if format == 'col':
                batch = self.collate(batch, cross_type)
            yield batch

    def collate(self, batch, cross_type):
        res1 = []

        cols = zip(*batch)
        for _ in range(4):
            res1.append(np.array(next(cols)))

        # 稀疏特征
        indice = next(cols)
        value = next(cols)
        indice2 = np.array([[i, y] for i, x in enumerate(indice) for y in x])
        value2 = np.array([y for x in value for y in x])
        if cross_type == 'sparse':
            sparse_matrix = coo_matrix((value2, zip(*indice2)), shape=(len(indice), config['cross_feature_num']))
            res1.append(sparse_matrix)
        elif cross_type == 'seperate':
            res1.append(indice2)
            res1.append(value2)
        else:
            res1.append(indice)
            res1.append(value)

        for _ in range(3):
            res1.append(np.array(next(cols)))

        res2 = np.array(next(cols))

        return res1, res2


def get_hdf5_dataloader(file, config, batch_size=None, format=None, random_read=None, cross_type=None):
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
    format = param_check(config, 'numpy_format', format, 'col')
    random_read = param_check(config, 'random_read', random_read, True)
    cross_type = param_check(config, 'cross_type', cross_type, 'sparse')

    generator = HDF5Generator(file, random_read=random_read)
    data_loader = HDF5toNumpy(generator)
    data_loader = data_loader.batching(batch_size, format,cross_type)
    return data_loader


if __name__ == '__main__':
    from demo.qier.code import param

    config = param.config

    file = '/root/rslib/demo/qier/code/dataset/2019-11-21.age_trainset.h5'
    config['cross_type'] = 'sparse'
    xx = get_hdf5_dataloader(file, config, batch_size=3)
    for i in xx:
        i
        print(len(i))
        print(i[1])
