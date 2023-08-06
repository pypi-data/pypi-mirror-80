import math
import random
import collections

import h5py
import numpy as np

from rslib.data.pytorch.tfrecord.util import reader
from rslib.data.pytorch.tfrecord.util import iterator_utils


def dataloader(data_path, description, index_path=None, shard=None, transform=None, shuffle_queue_size=None):
    it = reader.tfrecord_loader(
        data_path, index_path, description, shard)
    if shuffle_queue_size:
        it = iterator_utils.shuffle_iterator(it, shuffle_queue_size)
    if transform:
        it = map(transform, it)
    return it


# def get_tfrecord_dataloader(file, config, description=None, transform=None, shuffle_queue_size=1000):

class TFRecordGenerator(object):
    def __init__(self, file, config, random_read=True):
        self.file = file
        self.config = config
        self.random_read = random_read

    def __call__(self, description=None, transform=None, shuffle_queue_size=None):
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

        file = self.file
        config = self.config
        random_read = self.random_read
        if random_read:
            shuffle_queue_size = 10000

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
                for i in range(config['seq_num']):
                    sequence_id.append(np.pad(features["sequence_id_" + str(i)], (0, config['maxlen'] - len(features["sequence_id_" + str(i)])), 'constant', constant_values=(0, 0)).astype(np.int64))
                    sequence_time.append(np.pad(features["sequence_time_" + str(i)], (0, config['maxlen'] - len(features["sequence_time_" + str(i)])), 'constant', constant_values=(0, 0)).astype(np.int64))
                    sequence_time_gaps.append(np.pad(features["sequence_time_gaps_" + str(i)], (0, config['maxlen'] - len(features["sequence_time_gaps_" + str(i)])), 'constant', constant_values=(0, 0)).astype(np.int64))
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

        data_loader = dataloader(file, description=description, transform=transform, shuffle_queue_size=shuffle_queue_size)

        return data_loader
