#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""noising batched tokenized text for pytorch

    origin https://github.com/shentianxiao/text-autoencoders
"""

import numpy as np
import torch
from meguru_tokenizer.vocab import BaseVocab


class Noiser:
    """Noising per padded batch tensor

    Note:
        x is the torch.Tensor whose shape is [\|S\|, B]
    """

    def __init__(self, vocab: BaseVocab):
        self.unk_id = vocab.word2idx(vocab.unk)
        self.bos_id = vocab.word2idx(vocab.bos)
        self.pad_id = vocab.word2idx(vocab.pad)
        self.mask_id = vocab.word2idx(vocab.mask)

    def word_shuffle(self, x, k):  # slight shuffle such that |sigma[i]-i| <= k
        base = torch.arange(x.size(0), dtype=torch.float).repeat(x.size(1), 1).t()
        inc = (k + 1) * torch.rand(x.size())
        inc[x == self.bos_id] = 0  # do not shuffle the start sentence symbol
        inc[x == self.pad_id] = k + 1  # do not shuffle end paddings
        _, sigma = (base + inc).sort(dim=0)
        return x[sigma, torch.arange(x.size(1))]

    def word_drop(self, x, p):  # drop words with probability p
        x_ = []
        for i in range(x.size(1)):
            words = x[:, i].tolist()
            keep = np.random.rand(len(words)) > p
            keep[0] = True  # do not drop the start sentence symbol
            sent = [w for j, w in enumerate(words) if keep[j]]
            sent += [self.pad_id] * (len(words) - len(sent))
            x_.append(sent)
        return torch.LongTensor(x_).t().contiguous().to(x.device)

    def word_blank(self, x, p):  # blank words with probability p
        blank = (
            (torch.rand(x.size(), device=x.device) < p)
            & (x != self.bos_id)
            & (x != self.pad_id)
        )
        x_ = x.clone()
        x_[blank] = self.mask_id
        return x_

    def word_substitute(self, x, p):  # substitute words with probability p
        keep = (
            (torch.rand(x.size(), device=x.device) > p)
            | (x == self.bos_id)
            | (x == self.pad_id)
        )
        x_ = x.clone()
        x_.random_(0, len(vocab))
        x_[keep] = x[keep]
        return x_

    def noisy(self, x, drop_prob, blank_prob, sub_prob, shuffle_dist):
        if shuffle_dist > 0:
            x = self.word_shuffle(x, shuffle_dist)
        if drop_prob > 0:
            x = self.word_drop(x, drop_prob)
        if blank_prob > 0:
            x = self.word_blank(x, blank_prob)
        if sub_prob > 0:
            x = self.word_substitute(x, sub_prob)
        return x
