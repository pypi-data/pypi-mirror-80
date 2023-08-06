#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
FeatureUtil

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/9/11

Authors: zouzhene(zouzhene@corp.netease.com)
Phone: 13261632788
Date: 2020/3/11
"""
from tensorflow.python.data.ops import dataset_ops
import tensorflow as tf
import numpy as np
import re
import scipy
from tensorflow.python.keras.preprocessing import sequence


class FeatureUtil(object):
    '''
    构建数据集的工具类，构建的数据集以本地文件的方式进行存储。
    目前支持两种数据存储格式：tfrecord 和 hdf5。

    Args:
        config: 配置文件，定义了如下一些属性：
                    序列数量、

                    序列最大长度
    '''

    def __init__(self, config):
        self.config = config
        self.maxlen = config['maxlen']
        self.batchsize = config['batchsize']
        self.class_num = config['class_num']
        self.cross_feature_num = config['cross_feature_num']
        self.user_feature_num = config['user_feature_num']
        self.user_feature_size = config['user_feature_size']
        self.output_unit = config['output_unit']
        self.multi_class = config['multi_class']
        self.neg_sample = config['neg_sample']
        self.seq_num = self.config['seq_num']

    def feature_extraction(self, data, serving=False, write_to='hdf5'):
        '''
        从原始数据中提取特征，后续调用不同的方法将特征存储为 tfrecord 或者 hdf5 格式。

        Args:
            data: 原始数据
            predict: 是否预测阶段
            write_to: 'tfrecord' or 'hdf5'， 'tfrecord' default

        Returns:
            特征数据
        '''
        feature_id = {
            'role_id': 0,
            'role_id_hash': 1,
            'sequence_feature': 2,
            'cross_feature': 3,
            'user_feature': 4,
            'label': 5,
            'cur_time': 6,
            'weight': 7
        }

        role_id = [[int(sample.split('@')[feature_id['role_id']])] for sample in data]
        role_id_hash = [int(sample.split('@')[feature_id['role_id_hash']]) for sample in data]
        # pos_label = [int(sample.split('@')[feature_id['pos_label']].split(':')[0]) for sample in data]

        mask, label = [[int(x.split(':')[0]) for x in sample.split('@')[feature_id['label']].split(',')] for sample in data], \
                      [[int(x.split(':')[1]) for x in sample.split('@')[feature_id['label']].split(',')] for sample in data]

        cur_time = [int(sample.split('@')[feature_id['cur_time']]) for sample in data]

        sequence_id = [
            [[int(x.split(':')[0]) for x in
              sorted(re.split(', |,', xx), key=lambda x: x.split(':')[-1])][-self.maxlen:] if xx else [0] for xx in
             sample.split('@')[feature_id['sequence_feature']].split(';')[:self.seq_num]]
            for sample in data]
        sequence_time = [
            [[int(sample.split('@')[feature_id['cur_time']]) - int(x.split(':')[1]) for x in
              sorted(re.split(', |,', xx), key=lambda x: x.split(':')[-1])][-self.maxlen:] if xx else [0] for xx in
             sample.split('@')[feature_id['sequence_feature']].split(';')[:self.seq_num]]
            for sample in data]
        sequence_time_gaps = [[[0] + [abs(xx[i] - xx[i - 1]) for i in range(1, len(xx))] for xx in sample] for sample in sequence_time]

        cross_features_index = [[int(y.split(':')[0]) for y in re.split(', |,', sample.split('@')[feature_id['cross_feature']])] for sample in data]  # id+maxid*daygap
        cross_features_val = [[float(y.split(':')[1]) for y in re.split(', |,', sample.split('@')[feature_id['cross_feature']])] for sample in data]  # value
        user_features_id = [[int(y) if y else 0 for y in re.split(', |,', sample.split('@')[feature_id['user_feature']])] for sample in data]  # id+maxid*daygap
        user_features_id = [sample + [0] * (self.user_feature_num - len(sample)) for sample in user_features_id]
        # label_week_id = [[int(data[i].split('@')[feature_id['pos_label']].split(':')[1])] * len(sequence_id[i]) for i in range(len(data))]

        if serving:
            # 临时获取少量数据，
            # 在此处对稀疏向量做了 batch 处理
            cross_features_index = [[[i, int(y.split(':')[0])] for y in re.split(', |,', sample.split('@')[feature_id['cross_feature']])] for i, sample in enumerate(data)]
            cross_features_index, cross_features_val = self.cross_features_batch(cross_features_index, cross_features_val)
            # 序列特征，padding
            sequence_id = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post', dtype='int64') for x in sequence_id]
            sequence_time = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post', dtype='int64') for x in sequence_time]
            sequence_time_gaps = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post', dtype='int64') for x in sequence_time_gaps]
            # sequence_id = sequence.pad_sequences(sequence_id, maxlen=self.maxlen, padding='post')
            # sequence_time = sequence.pad_sequences(sequence_time, maxlen=self.maxlen, padding='post')
            # sequence_time_gaps = sequence.pad_sequences(sequence_time_gaps, maxlen=self.maxlen, padding='post')
            # mask、label，处理成 multi-hot
            mask, label = self.mask_label_multi_hot(mask, label)

            return np.array(role_id_hash), np.array(sequence_id), np.array(sequence_time), np.array(sequence_time_gaps), \
                   np.array(cross_features_index), np.array(cross_features_val), np.array(user_features_id), np.array(cur_time), \
                   np.array(mask), np.array(label)

        if write_to == 'hdf5':
            # 生成的特征用于写入hdf5
            # 稀疏特征，处理成 list of array
            cross_features_index = [np.array(item, dtype=np.int64) for item in cross_features_index]
            cross_features_val = [np.array(item, dtype=np.float32) for item in cross_features_val]
            # 序列特征，padding
            sequence_id = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post') for x in sequence_id]
            sequence_time = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post') for x in sequence_time]
            sequence_time_gaps = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post') for x in sequence_time_gaps]
            # mask、label，处理成 multi-hot
            mask, label = self.mask_label_multi_hot(mask, label)

            return np.array(role_id_hash, dtype=np.int64), np.array(sequence_id, dtype=np.int64), \
                   np.array(sequence_time, dtype=np.int64), np.array(sequence_time_gaps, dtype=np.int64), \
                   cross_features_index, cross_features_val, \
                   np.array(user_features_id, dtype=np.int64), np.array(cur_time, dtype=np.int64), \
                   np.array(mask), np.array(label)

        elif write_to == 'tfrecord':
            # 生成的特征用于写入tfrecord
            return role_id_hash, sequence_id, sequence_time, sequence_time_gaps, \
                   cross_features_index, cross_features_val, user_features_id, \
                   cur_time, mask, label

        else:
            raise Exception('feature_extraction get unexpected "write_to", %s not in ["hdf5", "tfrecord"]' % (write_to))

    def mask_label_multi_hot(self, mask, label):
        """Return the multi-hot of mask and label ids

        Args:
            mask: mask ids
            label: label ids

        Returns:
            multi-hot
        """
        mask_tmp = [[0] * self.output_unit for _ in range(len(mask))]
        label_tmp = [[0] * self.output_unit for _ in range(len(label))]
        for i, (line_mask, line_label) in enumerate(zip(mask, label)):
            for item_mask, item_label in zip(line_mask, line_label):
                mask_tmp[i][item_mask] = 1
                label_tmp[i][item_mask] = item_label
        return mask_tmp, label_tmp

    def cross_features_batch(self, index, val):
        """
        将稀疏特征处理成 batch 的形式，后续用于线上服务推理

        Args:
            index:稀疏特征的索引
            val:稀疏特征的值

        Returns:
            batched cross feature
        """
        batch_num = len(index)
        index = [b for a in index for b in a]
        val = [b for a in val for b in a]
        num = len(index)
        batch_size = (num - 1) // batch_num + 1

        index = [index[i * batch_size:(i + 1) * batch_size] for i in range(batch_num)]
        val = [val[i * batch_size:(i + 1) * batch_size] for i in range(batch_num)]
        for i in range(batch_num):
            if len(val[i]) == 0:
                index[i] = index[i - 1]
                val[i] = val[i - 1]
            elif len(val[i]) != batch_size:
                while len(val[i]) < batch_size:
                    index[i].append(index[i][-1])
                    val[i].append(val[i][-1])

        return index, val

    def to_tfrecord(self, csvfile, filename):
        """Extract features from the original data in csv format, and convert to tfrecord format.

        Note:
            Tensorflow uses tensorflow.TFRecordDataloader to load tfrecord files

            Pytorch uses pytorch.TFRecordDataloader to load tfrecord files

        Args:
            csv_file (str): the file, in which original csv data is saved
            h5_file (str): the file, to which tfrecord data will save

        Returns:

        """

        writer = tf.python_io.TFRecordWriter(filename)
        data = open(csvfile, 'r', encoding='utf8').read().split('\n')[1:-1]
        print('feature_extraction')
        for jj in range(1+len(data)//10000):
            role_id_hashs, sequence_ids, sequence_times, sequence_time_gapss, cross_features_indexs, cross_features_vals, user_features_ids, \
            cur_times, masks, labels = self.feature_extraction(data[jj*10000 : (jj+1)*10000], write_to='tfrecord')
            for i in range(len(role_id_hashs)):
                role_id_hash = role_id_hashs[i]
                sequence_id = sequence_ids[i]
                sequence_time = sequence_times[i]
                sequence_time_gaps = sequence_time_gapss[i]
                cross_features_index = cross_features_indexs[i]
                cross_features_val = cross_features_vals[i]
                user_features_id = user_features_ids[i]
                label = labels[i]
                mask = masks[i]
                cur_time = cur_times[i]

                sequence_id_feature = [tf.train.Feature(int64_list=tf.train.Int64List(value=sequence_id[i])) for i in range(self.seq_num)]
                sequence_time_feature = [tf.train.Feature(int64_list=tf.train.Int64List(value=sequence_time[i])) for i in range(self.seq_num)]
                sequence_time_gaps_feature = [tf.train.Feature(int64_list=tf.train.Int64List(value=sequence_time_gaps[i])) for i in range(self.seq_num)]

                role_id_hash_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=[role_id_hash]))
                cross_features_index_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=cross_features_index))
                cross_features_val_feature = tf.train.Feature(float_list=tf.train.FloatList(value=cross_features_val))
                user_features_id_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=user_features_id))
                label_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=label))
                mask_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=mask))
                cur_time_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=[cur_time]))

                feature = {
                    # 'hist_num': hist_num_feature,
                    'role_id_hash': role_id_hash_feature,
                    "cross_features_index": cross_features_index_feature,
                    "cross_features_val": cross_features_val_feature,
                    "user_features_id": user_features_id_feature,
                    'cur_time': cur_time_feature,
                    'mask': mask_feature,
                    "label": label_feature,
                }
                for seq_num_i in range(self.seq_num):
                    feature['sequence_id_' + str(seq_num_i)] = sequence_id_feature[seq_num_i]
                    feature['sequence_time_' + str(seq_num_i)] = sequence_time_feature[seq_num_i]
                    feature['sequence_time_gaps_' + str(seq_num_i)] = sequence_time_gaps_feature[seq_num_i]

                seq_example = tf.train.Example(
                    features=tf.train.Features(feature=feature)
                )
                writer.write(seq_example.SerializeToString())
        writer.close()

    def to_hdf5(self, csv_file, h5_file):
        """Extract features from the original data in csv format, and convert to hdf5 format.

        Note:
            Tensorflow uses tensorflow.HDF5Dataloader to load hdf5 files

            Pytorch uses pytorch.HDF5Dataloader to load hdf5 files

        Args:
            csv_file (str): the file, in which original csv data is saved
            h5_file (str): the file, to which hdf5 data will save

        Returns:

        """
        with open(csv_file, 'r', encoding='utf8') as iin:
            data = iin.read().split('\n')[1:-1]
            role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_features_index, cross_features_val, user_features_id, \
            cur_time, mask, label = self.feature_extraction(data, write_to='hdf5')

        import h5py
        with h5py.File(h5_file, 'w') as f:
            f.create_dataset('role_id_hash', data=np.array(role_id_hash))
            f.create_dataset('sequence_id', data=np.array(sequence_id))
            f.create_dataset('sequence_time', data=np.array(sequence_time))
            f.create_dataset('sequence_time_gaps', data=np.array(sequence_time_gaps))
            if len(set(len(x) for x in cross_features_index)) == 1:
                f.create_dataset('cross_features_index', data=cross_features_index)
                f.create_dataset('cross_features_val', data=cross_features_val)
            else:
                f.create_dataset('cross_features_index', data=cross_features_index, dtype=h5py.special_dtype(vlen=np.dtype('int64')))
                f.create_dataset('cross_features_val', data=cross_features_val, dtype=h5py.special_dtype(vlen=np.dtype('float32')))
            f.create_dataset('user_features_id', data=np.array(user_features_id))
            f.create_dataset('cur_time', data=np.array(cur_time))
            f.create_dataset('mask', data=np.array(mask))
            f.create_dataset('label', data=np.array(label))


if __name__ == '__main__':
    from demo.qier.code import param

    config = param.config
    file = '/root/rslib/demo/qier/code/dataset/2019-11-21.age_trainset.csv'
    tfrecord_file = '/root/rslib/demo/qier/code/dataset/2019-11-21.age_trainset.tfrecord'
    featureutil = FeatureUtil(config)
    featureutil.to_hdf5(file, tfrecord_file)
