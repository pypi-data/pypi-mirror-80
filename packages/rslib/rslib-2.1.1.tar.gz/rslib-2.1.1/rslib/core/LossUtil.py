#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
自定义的 Loss 函数

Authors: zouzhene(zouzhene@corp.netease.com)
Phone: 132****2788
Date: 2019/9/11
"""

import abc
import six
import tensorflow as tf
from tensorflow.python.distribute import distribution_strategy_context
from tensorflow.python.framework import ops
from tensorflow.python.framework import smart_cond
from tensorflow.python.framework import tensor_util
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.utils import losses_utils
from tensorflow.python.keras.utils import tf_utils
from tensorflow.python.keras.utils.generic_utils import deserialize_keras_object
from tensorflow.python.keras.utils.generic_utils import serialize_keras_object
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import nn
from tensorflow.python.ops.losses import losses_impl
from tensorflow.python.ops.losses import util as tf_losses_util
from tensorflow.python.util.tf_export import keras_export
from tensorflow.tools.docs import doc_controls
from tensorflow.python.keras.backend import _constant_to_tensor, epsilon
from tensorflow.python.ops import clip_ops


def masked_categorical_crossentropy(y_true,
                                    y_pred,
                                    mask_value=-1):
    '''支持掩码的分类损失函数

    Args:
        y_true:真实值
        y_pred:预测值
        mask_value:掩码。真实值中与掩码相同的部分，不计入损失函数

    Returns:

    '''
    y_true = math_ops.cast(y_true, y_pred.dtype)
    y_pred = ops.convert_to_tensor(y_pred)
    mask = K.cast(K.not_equal(y_true, mask_value), K.floatx())

    output = tf.multiply(tf.exp(y_pred), mask)
    output = output / math_ops.reduce_sum(output, -1, True)
    # Compute cross entropy from probabilities.
    epsilon_ = _constant_to_tensor(epsilon(), output.dtype.base_dtype)
    output = clip_ops.clip_by_value(output, epsilon_, 1. - epsilon_)
    return -math_ops.reduce_sum(y_true * math_ops.log(output), -1)
