#!/usr/bin/env python3

from pathlib import Path
from typing import List, Tuple, Optional
from meguru_tokenizer.base_tokenizer import Tokenizer
import sentencepiece as spm
from meguru_tokenizer.vocab import BaseVocab


class SentencePieceVocab(BaseVocab):
    def __init__(self, sp: spm.SentencePieceProcessor):
        super().__init__()
        self.sp = sp

    def __len__(self):
        return len(self.sp)

    def word2idx(self, word: str):
        return self.sp.PieceToId(word)

    def idx2word(self, idx: int):
        return self.sp.IdToPiece(idx)


class SentencePieceTokenizer(Tokenizer):
    """tokenizer splits by SentencePiece

    Examples:

            >>> tokenizer = SentencePieceTokenizer(lower=True, language="ja")
            >>> sentences = [
            >>>     "Hello, I don't know how to use it?",
            >>>     "Tensorflow is awesome!",
            >>>     "it is good framework.",
            >>> ]
            >>> source_file = Path("test.txt")
            >>> with source_file.open("w", encoding="utf-8") as f:
            >>>     for s in sentences:
            >>>         f.write(s + "\\n")
            >>> tokenizer.train_sp(source_file, vocab_size=37)
            >>> print("vocabs:")
            >>> with Path("m.vocab").open("r", encoding="utf-8") as f:
            >>>     line = f.readline()
            >>>     while line:
            >>>         w, idx = line.strip().split()
            >>>         print(f"{w} {idx}")
            >>>         line = f.readline()
            vocabs:
            <pad> 0
            <s> 0
            </s> 0
            <unk> 0
            <mask> 0
            ▁ -1.85354
            o -2.41476
            ...
            >>> print("tokenized sentence")
            >>> print(tokenizer.tokenize_list(sentences))
            [['▁', 'h', 'e', 'l', 'lo', ',', '▁i', '▁', ...
            >>> print("encoded sentence")
            >>> print([tokenizer.encode(sentence) for sentence in sentences])
            [[5, 31, 9, 22, 19, 25, 12, 5, 13, 6, 10, ...
            >>> pretokens = [tokenizer.encode(sentence) for sentence in sentences]
            >>> print("decode sentence")
            >>> print([tokenizer.decode(tokens) for tokens in pretokens])
            ["hello, i don't know how to use it?", 'tensorflow is awesome!', 'it is good framework.']
            >>> print("reload from dump file")
            >>> tokenizer = SentencePieceTokenizer(lower=True, language="ja")
            >>> tokenizer.load_sp_model("m")
            >>> print("tokenized sentence")
            >>> print(tokenizer.tokenize_list(sentences))
            [['▁', 'h', 'e', 'l', 'lo', ',', '▁i', '▁', ...
            >>> print("encoded sentence")
            >>> print([tokenizer.encode(sentence) for sentence in sentences])
            [[5, 31, 9, 22, 19, 25, 12, 5, 13, 6, 10, ...
            >>> assert pretokens == [tokenizer.encode(sentence) for sentence in sentences]
    """

    languages = ["ja", "en", "de"]

    def __init__(
        self, normalize: bool = True, lower: bool = True, language: str = "unk",
    ):
        super().__init__(normalize=normalize, lower=lower, language=language)

    def vocab_size(self):
        return len(self.vocab)

    def tokenize(self, sentence: str):
        sentence = self._normalize(sentence) if self.normalize else sentence
        return self.vocab.sp.EncodeAsPieces(sentence)

    def tokenize_list(self, sentences: List[str]):
        return [self.tokenize(sentence) for sentence in sentences]

    def encode(self, sentence: str):
        sentence = self._normalize(sentence) if self.normalize else sentence
        return self.vocab.sp.EncodeAsIds(sentence)

    def decode(self, tokens: List[int]):
        return self.vocab.sp.DecodeIds(tokens)

    def load_sp_model(self, prefix: str):
        sp = spm.SentencePieceProcessor()
        sp.Load(prefix + ".model")
        self.vocab = SentencePieceVocab(sp)

    def train_sp(
        self,
        resource_flile: str,
        model_prefix: str = "m",
        vocab_size: int = 8000,
        character_coverage: float = 0.995,
        model_type="unigram",
        user_defined_symbols: Tuple[str] = ("<mask>"),
    ):
        """train sentencepiece model

        Args:
           resource_file (str): file for training sentencepiece
           vocab_size (int): vocaburary size e.g. 8000, 16000
           character_coverage (float) : character coverage [0, 1] default 0.995
           model_type (str) : ['unigram', 'char', 'bpe', 'word']
                              ref. https://github.com/google/sentencepiece
           user_defined_symbols (List[str]) : special tokens such as "<mask>"

        Note:
           resource_file's is "sentence per line"
           pre_defined_symbols : <UNK>, <s>, </s>, <pad>
        """
        parameters = [
            f"--input={resource_flile}",
            f"--model_prefix={model_prefix}",
            "--pad_id=0",
            "--unk_id=3",
            f"--vocab_size={vocab_size}",
            f"--character_coverage={character_coverage}",
            f"--model_type={model_type}",
        ]
        if user_defined_symbols is not None:
            user_defined_symbols = ["<mask>"]
        user_defined_symbols = ",".join(user_defined_symbols)
        parameters.append(f"--user_defined_symbols={user_defined_symbols}")
        parameter = " ".join(parameters)
        spm.SentencePieceTrainer.Train(parameter)
        self.load_sp_model(model_prefix)


if __name__ == "__main__":

    tokenizer = SentencePieceTokenizer(lower=True, language="en")
    sentences = [
        "Hello, I don't know how to use it?",
        "Tensorflow is awesome!",
        "it is good framework.",
    ]
    source_file = Path("test.txt")
    with source_file.open("w", encoding="utf-8") as f:
        for s in sentences:
            f.write(s + "\n")

    tokenizer.train_sp(source_file, vocab_size=37)

    print("vocabs:")
    with Path("m.vocab").open("r", encoding="utf-8") as f:
        line = f.readline()
        while line:
            w, idx = line.strip().split()
            print(f"{w} {idx}")
            line = f.readline()
    print("tokenized sentence")
    print(tokenizer.tokenize_list(sentences))
    print("encoded sentence")
    print([tokenizer.encode(sentence) for sentence in sentences])
    pretokens = [tokenizer.encode(sentence) for sentence in sentences]
    print("decode sentence")
    print([tokenizer.decode(tokens) for tokens in pretokens])
    print("reload from dump file")
    tokenizer = SentencePieceTokenizer(lower=True, language="ja")
    tokenizer.load_sp_model("m")
    print("tokenized sentence")
    print(tokenizer.tokenize_list(sentences))
    print("encoded sentence")
    print([tokenizer.encode(sentence) for sentence in sentences])
    assert pretokens == [tokenizer.encode(sentence) for sentence in sentences]
