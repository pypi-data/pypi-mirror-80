#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# @File    :   transformer.py    
# @Contact :   zouzhene@corp.netease.com
# @License :   Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
#              Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
# 
# @Modify Time      @Author    @Version    @Desciption
# ------------      -------    --------    -----------
# 2020/6/29 15:28   zouzhene    1.0         None

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.onnx

torch.onnx.export

from rslib.algo.pytorch.sparse.sparse_linear import SparseLinear


class TransformerNet(torch.nn.Module):
    def __init__(self, ww=None):
        super(TransformerNet, self).__init__()
        self.embedding0 = torch.nn.Embedding(1000, 64)
        self.emb_linear = torch.nn.Linear(64, 256)

        encoder_layer = nn.TransformerEncoderLayer(d_model=256, nhead=4)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=2)

        self.linear_1 = torch.nn.Linear(256, 128)
        self.linear_2 = torch.nn.Linear(128, 128)

        self.hidden_1 = torch.nn.Linear(128, 128)
        self.output_1 = torch.nn.Linear(128, 10)

    def forward(self, role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_features_index, cross_features_val,
                user_features_id, cur_time):
        create_id = sequence_id[:, 0]
        create_mask = sequence_time[:, 0] > 0
        create_id_emb = self.embedding0(create_id)
        create_id_emb = self.emb_linear(create_id_emb)

        # create_id_emb_att = self.transformer_encoder(create_id_emb.permute([1, 0, 2]))
        create_id_emb_att = self.transformer_encoder(create_id_emb.permute([1, 0, 2]), src_key_padding_mask=~create_mask)
        create_id_emb_att = create_id_emb_att.permute([1, 0, 2])

        x = create_id_emb_att
        create_mask2 = torch.unsqueeze(create_mask, 2)
        mask_sum = (create_mask2 * x).sum(1)
        mask_mean = mask_sum / create_mask.sum(1, keepdim=True)

        h = F.relu(self.linear_1(mask_mean))
        h = F.relu(self.linear_2(h))

        h_1 = F.relu(self.hidden_1(h))
        logits_1 = self.output_1(h_1)

        return logits_1
