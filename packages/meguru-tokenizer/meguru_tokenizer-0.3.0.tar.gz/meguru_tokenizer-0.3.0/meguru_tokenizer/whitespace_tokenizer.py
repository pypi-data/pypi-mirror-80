#!/usr/bin/env python3

from pathlib import Path
from typing import List, Optional
from meguru_tokenizer.base_tokenizer import Tokenizer
from meguru_tokenizer.vocab import Vocab
import neologdn
import unicodedata
import nltk


class WhitespaceTokenizer(Tokenizer):
    """tokenizer splits by whitespace

    Example:

        >>> import pprint
        >>> tokenizer = WhitespaceTokenizer(lower=True, language="en")
        >>> sentences = [
        >>>     "Hello, I don't know how to use it?",
        >>>     "Tensorflow is awesome!",
        >>>     "it is good framework.",
        >>>  ]
        >>> vocab = Vocab()
        >>> for sentence in sentences:
                vocab.add_vocabs(tokenizer.tokenize(sentence))
        >>> vocab.build_vocab()
        >>> tokenizer.vocab = vocab
        >>> vocab.dump_vocab(Path("vocab.txt"))
        >>> print("vocabs:")
        >>> pprint.pprint(vocab.i2w)
        {0: '<pad>',
         1: '<s>',
         2: '</s>',
         3: '<unk>',
         4: '<mask>',
         5: 'it',
         6: 'is',
         7: 'hello',
         8: ',',
         9: 'i',
         10: 'do',
         11: "n't",
         12: 'know',
         13: 'how',
         14: 'to',
         15: 'use',
         16: '?',
         17: 'tensorflow',
         18: 'awesome',
         19: '!',
         20: 'good',
         21: 'framework',
         22: '.'}
        >>> print("tokenized sentence")
        >>> pprint.pprint(tokenizer.tokenize_list(sentences))
        [['hello', ',', 'i', 'do', "n't", 'know', 'how', 'to', 'use', 'it', '?'],
         ['tensorflow', 'is', 'awesome', '!'],
         ['it', 'is', 'good', 'framework', '.']]
        >>> print("encoded sentence")
        >>> pprint.pprint([tokenizer.encode(sentence) for sentence in sentences])>
        [[7, 8, 9, 10, 11, 12, 13, 14, 15, 5, 16], [17, 6, 18, 19], [5, 6, 20, 21, 22]]
        >>> encodes = []
        >>> for sentence in sentences:
        >>>     encodes.append(tokenizer.encode(sentence))
        >>> print("decoded sentence")
        >>> pprint.pprint([tokenizer.decode(tokens) for tokens in encodes])
        ["hello , i do n't know how to use it ?",
         'tensorflow is awesome !',
         'it is good framework .']
    """

    languages = ["en", "de"]

    def __init__(
        self,
        vocab: Optional[Vocab] = None,
        normalize: bool = True,
        lower: bool = True,
        language: str = "unk",
    ):
        super().__init__(normalize=normalize, lower=lower, language=language)
        self.vocab = vocab
        self.tokenizer = nltk.tokenize.NLTKWordTokenizer()

    def tokenize(self, sentence: str):
        sentence = self._normalize(sentence) if self.normalize else sentence
        return list(self.tokenizer.tokenize(sentence))

    def tokenize_list(self, sentences: List[str]):
        return [self.tokenize(sentence) for sentence in sentences]

    def vocab_size(self):
        return len(self.vocab)

    def encode(self, sentence: str):
        if self.vocab is None:
            raise NotImplementedError()
        words = self.tokenize(sentence)
        return [self.vocab.word2idx(word) for word in words]

    def decode(self, tokens: List[int]):
        if self.vocab is None:
            raise NotImplementedError()
        words = [self.vocab.idx2word(idx) for idx in tokens]
        return " ".join(words)


class LooseWhitespaceTokenizer(WhitespaceTokenizer):
    """tokenizer splits by whitespace (without NLTK tokenize)
    """

    languages = ["en", "de", "ja"]

    def __init__(
        self,
        vocab: Optional[Vocab] = None,
        normalize: bool = True,
        lower: bool = True,
        language: str = "unk",
    ):
        super().__init__(
            vocab=vocab, normalize=normalize, lower=lower, language=language
        )

    def tokenize(self, sentence: str):
        sentence = self._normalize(sentence) if self.normalize else sentence
        return sentence.strip().split()


if __name__ == "__main__":
    import pprint

    tokenizer = WhitespaceTokenizer(lower=True, language="en")
    sentences = [
        "Hello, I don't know how to use it?",
        "Tensorflow is awesome!",
        "it is good framework.",
    ]
    vocab = Vocab()

    for sentence in sentences:
        vocab.add_vocabs(tokenizer.tokenize(sentence))
    vocab.build_vocab()

    tokenizer.vocab = vocab
    vocab.dump_vocab(Path("vocab.txt"))
    print("vocabs:")
    pprint.pprint(vocab.i2w)

    print("tokenized sentence")
    pprint.pprint(tokenizer.tokenize_list(sentences))
    print("encoded sentence")
    pprint.pprint([tokenizer.encode(sentence) for sentence in sentences])

    encodes = []
    for sentence in sentences:
        encodes.append(tokenizer.encode(sentence))

    print("decoded sentence")
    pprint.pprint([tokenizer.decode(tokens) for tokens in encodes])

    vocab_size = len(vocab)
    print("reload from dump file")
    vocab = Vocab()
    vocab.load_vocab(Path("vocab.txt"))
    assert vocab_size == len(vocab)
    tokenizer = WhitespaceTokenizer(vocab=vocab, language="en")
    pprint.pprint([tokenizer.encode(sentence) for sentence in sentences])

    vocab = Vocab()
    for sentence in sentences:
        vocab.add_vocabs(tokenizer.tokenize(sentence))
    vocab.build_vocab(min_freq=2)
    assert vocab_size != len(vocab)

    vocab = Vocab()
    for sentence in sentences:
        vocab.add_vocabs(tokenizer.tokenize(sentence))
    vocab.build_vocab(vocab_size=10)
    assert 10 == len(vocab)
