#!/usr/bin/env python3

from typing import List
import numpy as np
import tensorflow as tf
from meguru_tokenizer.vocab import BaseVocab


class Noiser:
    """Noising per tokenized sentnece

    Note:
        x is the np.array whose shape is [\|S\|,]
        \|S\| is a variable sequence length
    """

    def __init__(self, vocab: BaseVocab):
        self.unk_id = vocab.word2idx(vocab.unk)
        self.bos_id = vocab.word2idx(vocab.bos)
        self.pad_id = vocab.word2idx(vocab.pad)
        self.mask_id = vocab.word2idx(vocab.mask)
        self.vocab = vocab
        self.vocab_size = len(vocab)

    def word_shuffle(self, x: np.ndarray, k: float):
        """slight shuffle such that \|sigma[i]-i\| <= k

        Args:
            x (np.ndarray): [None, ] encoded sentence
            k      (float): shuffle probability [0, inf) \n
                | if k << 0, shuffle frequency is low

        Returns:
            np.ndarray: shuffled array [None, ]
        """
        base = np.arange(x.shape[0], dtype=np.float)
        inc = (k + 1) * tf.random.uniform(x.shape)
        sigma = np.argsort(base + inc)
        return x[sigma]

    def word_drop(self, x: np.ndarray, p: float):
        """drop words with probability p

        Args:
            x (np.ndarray): [None, ] encoded sentence
            p      (float): drop rate \n
                | if 1 - p << 0, drop rate is high \n
                | if p << 0, drop rate is low

        Returns:
            np.ndarray: drop array [None, ]
        """
        words = x.tolist()
        keep = tf.random.uniform([len(words)]) > p
        sent = [w for j, w in enumerate(words) if keep[j]]
        x = np.array(sent)
        return x

    def word_blank(self, x: np.ndarray, p: float):
        """blank words with probability p

        Args:
            x (np.ndarray): [None, ] encoded sentence
            p      (float): blank rate \n
                | if 1 - p << 0, drop rate is high \n
                | if p << 0, drop rate is low

        Returns:
            np.ndarray: [None, ] blank array
        """
        blank = tf.random.uniform(x.shape) < p
        x[blank.numpy().tolist()] = self.mask_id
        return x

    def word_substitute(self, x: np.ndarray, p: float):
        """substitute words with probability p

        Args:
            x (np.ndarray): [None, ] encoded sentence
            p      (float): substitute rate \n
                | if 1 - p << 0, drop rate is high \n
                | if p << 0, drop rate is low

        Returns:
            np.ndarray: [None, ] substitute array
        """
        keep = tf.random.uniform(x.shape) > p
        # 5 means the vocaburary without extra wods
        x_ = [
            idx if idx < 5 else self.unk_id
            for idx in tf.random.uniform(
                x.shape, minval=0, maxval=self.vocab_size, dtype=tf.int64
            )
        ]
        x_ = np.array(x_)
        x_[keep.numpy().tolist()] = x[keep.numpy().tolist()]
        return x_

    def noisy(
        self,
        x: List[int],
        drop_prob: float,
        blank_prob: float,
        sub_prob: float,
        shuffle_dist: float,
    ):
        """add noise

        Args:
            x     (List[int]): list of word-index without any extra token (unk is ok)
            drop_prob (float): drop rate [0, 1)
            blank_prob (float): blank rate [0, 1)
            sub_prob (float): substitute rate [0, 1)
            shuffle_dist (float): shuffle rate [0, inf)

        Returns:
            np.ndarray: [None, ] noised x
        """
        x = np.array(x)
        if shuffle_dist > 0:
            x = self.word_shuffle(x, shuffle_dist)
        if drop_prob > 0:
            x = self.word_drop(x, drop_prob)
        if blank_prob > 0:
            x = self.word_blank(x, blank_prob)
        if sub_prob > 0:
            x = self.word_substitute(x, sub_prob)
        return x


if __name__ == "__main__":
    from pprint import pprint
    from pathlib import Path
    import re
    from meguru_tokenizer.whitespace_tokenizer import WhitespaceTokenizer
    from meguru_tokenizer.vocab import Vocab

    sentences = [
        "Hello, I don't know how to use it?",
        "Tensorflow is awesome!",
        "It is good framework.",
    ]

    tokenizer = WhitespaceTokenizer(lower=True, language="en")
    vocab = Vocab()

    with Path("decl_independance.txt").open("w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + "\n")

    for sentence in sentences:
        vocab.add_vocabs(tokenizer.tokenize(sentence))
    vocab.build_vocab(vocab_size=30)

    tokenizer.vocab = vocab

    # for sentence in sentences:
    #     print(tokenizer.decode((tokenizer.encode(sentence))))

    noiser = Noiser(vocab=tokenizer.vocab)

    # for sentence in sentences:
    #     print(len(noiser.noisy(tokenizer.tokenize(sentence), 0.3, 0, 0, 0)))

    ds = tf.data.TextLineDataset("decl_independance.txt")
    bos_id = tokenizer.vocab.word2idx(tokenizer.vocab.bos)
    print("bos id ", bos_id)

    def encode(text):
        encoded_text = tokenizer.encode(text.numpy().decode())
        # print(
        #     "[base]\n",
        #     encoded_text,
        #     "\n",
        #     text.numpy().decode(),
        #     "==",
        #     tokenizer.decode(encoded_text),
        # )
        encoded_text = noiser.noisy(encoded_text, 0, 0.8, 0, 0)
        print(
            "[noised]\n",
            encoded_text,
            "\n",
            text.numpy().decode(),
            "->",
            tokenizer.decode(np.concatenate(([bos_id], encoded_text))),
        )
        return np.concatenate(([bos_id], encoded_text))

    def encoded_map_fn(text):
        encoded_text = tf.py_function(encode, inp=[text], Tout=(tf.int64))
        encoded_text.set_shape([None])
        return encoded_text

    encoded_ds = ds.map(encoded_map_fn).padded_batch(3)

    for epoch in range(3):
        print("epoch :", epoch)
        for batch in encoded_ds:
            print("[padded batch]")
            print(batch)
