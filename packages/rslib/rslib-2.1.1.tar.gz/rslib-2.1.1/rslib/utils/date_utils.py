#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The nsh-item Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
时间处理工具

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/2/18
"""

import datetime
from dateutil.relativedelta import relativedelta


def date_add(date, i):
    '''
    对 日期 做加法

    Args:
        date:日期
        i: 增加的日期

    Returns:

    '''
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    return (d + relativedelta(days=i)).strftime('%Y-%m-%d')


def date_sub(date, i):
    '''
    对 日期 做减法

    Args:
        date: 日期
        i: 减少的日期

    Returns:

    '''
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    return (d - relativedelta(days=i)).strftime('%Y-%m-%d')
