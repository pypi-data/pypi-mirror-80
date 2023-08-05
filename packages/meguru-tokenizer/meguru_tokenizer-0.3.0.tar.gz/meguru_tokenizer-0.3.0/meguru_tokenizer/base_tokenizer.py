#!/usr/bin/env python3


import unicodedata
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
from neologdn import normalize


class Tokenizer(ABC):
    """Base Tokenizer

    Attributes:
        tokenizer: tokenizer e.g. MeCab, Sudachi
    
    """

    languages = []

    def __init__(self, normalize: bool, lower: bool, language: str = "unk"):
        """"""
        if language not in self.languages:
            raise NotImplementedError(
                "{} is not in {}".format(language, self.languages)
            )

        self.tokenizer = None
        self.lower = lower
        self.normalize = normalize

    @abstractmethod
    def vocab_size(self):
        """vocaburary size

        Returns:
            int: vocab_size
        """
        raise NotImplementedError()

    @abstractmethod
    def encode(self, sentnece: str):
        """encode a sentence

        Args:
            sentnece (str): a sentence

        Returns:
            List[int]: tokens

        Example:

            >>> tokenize.tokenizer("おはようございます。")
            [2, 3, 1, 4]

        """
        NotImplementedError()

    @abstractmethod
    def decode(self, tokens: List[int]):
        """decode a sentence

        Args:
            tokens (List[int]): tokens

        Returns:
            str: a sentence

        Example:

            >>> tokenize.tokenizer([2, 3, 1, 4])
            "おはようございます。"

        """
        NotImplementedError()

    def _normalize(self, sentence: str):
        sentence = normalize(sentence)

        if self.lower:
            sentence = sentence.lower()

        # sentence = unicodedata.normalize("NFKD", sentence)
        # NFKD in japanese : が -> か + "
        # NFKC in japanese : が -> が
        sentence = unicodedata.normalize("NFKC", sentence)
        return sentence

    def tokenize(self, sentence: str):
        """tokenize a sentence

        Args:
            sentence (str): a sentence

        Returns:
            List[str]: words

        Example:

            >>> tokenizer.tokenize("おはようございます。")
            ["おはよう", "ござい", "ます", "。"]

        """
        return sentence.split()

    def tokenize_list(self, sentences: List[str]):
        """tokenize list of sentence
        Args:
            sentences (List[str]): sentence list

        Returns:
            List[List[str]]: list of listed words

        Examples:

            >>> tokenizer.tokenize(["おはようございます。"])
            [["おはよう", "ござい", "ます", "。"]]

        """
        return [self.tokenize(sentence) for sentence in sentences]
