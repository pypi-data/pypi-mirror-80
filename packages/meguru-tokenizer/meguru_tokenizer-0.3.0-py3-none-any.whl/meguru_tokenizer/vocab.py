#!/usr/bin/env python3
from abc import abstractmethod
from pathlib import Path
from typing import List, Optional
from collections import Counter
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BaseVocab:
    def __init__(
        self,
        unk: str = "<unk>",
        pad: str = "<pad>",
        bos: str = "<s>",
        eos: str = "</s>",
        mask: str = "<mask>",
    ):
        # extra vocab
        self.unk = unk
        self.pad = pad
        self.bos = bos
        self.eos = eos
        self.mask = mask
        self.extra_vocab = [self.pad, self.bos, self.eos, self.unk, self.mask]

    @abstractmethod
    def word2idx(self, word: str):
        raise NotImplementedError()

    @abstractmethod
    def idx2word(self, idx: int):
        raise NotImplementedError()


class Vocab(BaseVocab):
    def __init__(
        self,
        unk: str = "<unk>",
        pad: str = "<pad>",
        bos: str = "<s>",
        eos: str = "</s>",
        mask: str = "<mask>",
    ):
        super().__init__(unk, pad, bos, eos, mask)

        self.vocab_base = []
        self.w2i = {}
        self.i2w = {}

    def __len__(self):
        return len(self.w2i)

    def word2idx(self, word: str):
        """word to index

        Args:
           word (str): a word

        Returns:
           int: the idx which pairs of the word
           if idx is not found, will return the idx of "<unk>"
        """
        return self.w2i.get(word, self.w2i[self.unk])

    def idx2word(self, idx: int):
        """word to index

        Args:
           idx (int): index of the word

        Returns:
           str: the word which pairs of the word
           if the word is not found, will return "<unk>"
        """
        return self.i2w.get(idx, self.unk)

    def add_vocab(self, word: str):
        """add a word into vocaburary to construct vocaburary list

        Args:
           word (str): a word
        """
        self.vocab_base.append(word)

    def add_vocabs(self, words: List[str]):
        """add a words into vocaburary to construct vocaburary list

        Args:
           words (List[str]): list of word

        Example:

           >>> words = sentence.split()
           >>> vocab.add_vocabs(words)
        """
        for word in words:
            self.add_vocab(word)

    def build_vocab(
        self, min_freq: Optional[int] = None, vocab_size: Optional[int] = None,
    ):
        """build vocaburary list from added vocabs

        Args:
            min_freq (Optional[int]): minimum frequency of the vocab
            vocab_size (Optional[int]): maximum vocaburary size

        Note:
           when vocaburary is builded,
           the source of vocaburary will be removed to free memory space.
        """
        for w in self.extra_vocab:
            self.w2i[w] = len(self.w2i)
            self.i2w[len(self.w2i) - 1] = w

        vocab_counter = Counter(self.vocab_base)
        for idx, (w, c) in enumerate(vocab_counter.most_common()):
            if min_freq is not None and c < min_freq:
                break
            if vocab_size is not None and idx >= vocab_size - len(self.extra_vocab):
                break
            self.w2i[w] = len(self.w2i)
            self.i2w[len(self.w2i) - 1] = w
        logger.info("vocab_size {}".format(len(self.w2i)))
        self.vocab_base = []

    def dump_vocab(self, export_path: Path):
        """dump vocab

        Args:
            export_path (Path):
        """
        with export_path.open("w", encoding="utf-8") as f:
            for word, idx in self.w2i.items():
                f.write("{}\t{}\n".format(word, idx))

    def load_vocab(self, load_path: Path):
        """dump vocab

        Args:
            load_path (Path):
        """
        self.w2i = {}
        self.i2w = {}
        with load_path.open("r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                word, idx = line.strip().split("\t")
                idx = int(idx)
                self.w2i[word] = idx
                self.i2w[idx] = word
                line = f.readline()
        logger.info("vocab_size {}".format(len(self.w2i)))
