import math
import random
import collections

import h5py
import numpy as np


class HDF5Generator(object):
    def __init__(self, file, chunk_size=1000, worker_num=4, random_read=True):
        self.file = file
        self.chunk_size = chunk_size
        self.work_num = worker_num
        self.random_read = random_read

        with h5py.File(self.file, 'r') as file:
            self.length = len(file['label'])

    def __call__(self):
        chunk_size = self.chunk_size
        worker_num = self.work_num
        length = self.length
        random_read = self.random_read

        with h5py.File(self.file, 'r') as file:
            chunk_num = int(math.ceil(length / float(chunk_size)))
            worker_num = min(worker_num, chunk_num)

            chunk_ids = np.arange(chunk_num)
            if random_read:
                np.random.shuffle(chunk_ids)

            random_chunk_ids = collections.deque(chunk_ids)

            colum_name = ['role_id_hash', 'sequence_id', 'sequence_time', 'sequence_time_gaps', 'cross_features_index',
                          'cross_features_val', 'user_features_id', 'cur_time', 'mask', 'label']
            queue_worker = [{'chunk_id': i,  # 0
                             'chunk_in_id': 0,  # 1
                             'chunk_length': min(chunk_size * (i + 1), length) - chunk_size * i,  # 2
                             'chunk_data': list(zip(*[file[n][chunk_size * i:  min(chunk_size * (i + 1), length)] for n in colum_name])),  # 5
                             'chunk_in_id_random': np.random.permutation(np.arange(min(chunk_size * (i + 1), length) - chunk_size * i))
                             }
                            for _ in range(worker_num) for i in [random_chunk_ids.popleft()]]

            np.random.permutation(np.arange(self.length))
            for _ in range(length):
                cur_worker = random.randint(0, len(queue_worker) - 1)
                chunk_in_id = queue_worker[cur_worker]['chunk_in_id']
                chunk_in_id_random = queue_worker[cur_worker]['chunk_in_id_random'][chunk_in_id]
                if random_read:
                    data = queue_worker[cur_worker]['chunk_data'][chunk_in_id_random]
                else:
                    data = queue_worker[cur_worker]['chunk_data'][chunk_in_id]
                yield data
                queue_worker[cur_worker]['chunk_in_id'] += 1
                if queue_worker[cur_worker]['chunk_in_id'] == queue_worker[cur_worker]['chunk_length']:
                    del queue_worker[cur_worker]
                    if random_chunk_ids:
                        queue_worker.extend([{'chunk_id': i,  # 0
                                              'chunk_in_id': 0,  # 1
                                              'chunk_length': min(chunk_size * (i + 1), length) - chunk_size * i,  # 2
                                              'chunk_data': list(zip(*[file[n][chunk_size * i:  min(chunk_size * (i + 1), length)] for n in colum_name])),  # 5
                                              'chunk_in_id_random': np.random.permutation(np.arange(min(chunk_size * (i + 1), length) - chunk_size * i))
                                              }
                                             for i in [random_chunk_ids.popleft()]])
