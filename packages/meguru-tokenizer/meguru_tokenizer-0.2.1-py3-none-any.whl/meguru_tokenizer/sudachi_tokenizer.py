#!/usr/bin/env python3

from typing import List, Optional
from ginza.sudachipy_tokenizer import SUDACHIPY_DEFAULT_SPLIT_MODE
from ginza.command_line import Analyzer
from meguru_tokenizer.base_tokenizer import Tokenizer
from meguru_tokenizer.vocab import Vocab
from pathlib import Path


class SudachiTokenizer(Tokenizer):
    """tokenizer splits by sudachi

    Example:

        >>> import pprint
        >>> tokenizer = SudachiTokenizer(language="ja")
        >>> sentences = ["銀座でランチをご一緒しましょう。", "締切間に合いますか？", "トークナイザを作りました。"]
        >>> vocab = Vocab()
        >>> for sentence in sentences:
        >>>     vocab.add_vocabs(tokenizer.tokenize(sentence))
        >>> vocab.build_vocab()
        >>> tokenizer.vocab = vocab
        >>> vocab.dump_vocab(Path("vocab.txt"))
        >>> print("vocabs:")
        >>> pprint.pprint(vocab.i2w)
        vocabs:
        {0: '<pad>',
         1: '<s>',
         2: '</s>',
         3: '<unk>',
         4: '<mask>',
         5: 'を',
         6: '。',
         7: '銀座',
         8: 'で',
         9: 'ランチ',
         10: 'ご',
         11: '一緒',
         12: 'し',
         13: 'ましょう',
         14: '締切',
         15: '間に合い',
         16: 'ます',
         17: 'か',
         18: '?',
         19: 'トークナイザ',
         20: '作り',
         21: 'まし',
         22: 'た'}        >>> print("tokenized sentence")
        >>> pprint.pprint(tokenizer.tokenize_list(sentences))
        >>> print("encoded sentence")
        [['銀座', 'で', 'ランチ', 'を', 'ご', '一緒', 'し', 'ましょう', '。'],
         ['締切', '間に合い', 'ます', 'か', '?'],
         ['トークナイザ', 'を', '作り', 'まし', 'た', '。']]
        >>> pprint.pprint([tokenizer.encode(sentence) for sentence in sentences])
        [[19, 5, 20, 21, 22, 6], [19, 5, 20, 21, 22, 6], [19, 5, 20, 21, 22, 6]]
        >>> encodes = []
        >>> for sentence in sentences:
        >>>     encodes.append(tokenizer.encode(sentence))
        >>> print("decoded sentence")
        >>> pprint.pprint([tokenizer.decode(tokens) for tokens in encodes])
        ['銀座 で ランチ を ご 一緒 し ましょう 。', '締切 間に合い ます か ?', 'トークナイザ を 作り まし た 。']
    """

    languages = ["ja"]

    def __init__(
        self,
        vocab: Optional[Vocab] = None,
        normalize: bool = True,
        sudachi_normalize: bool = False,
        lower: bool = False,
        language: bool = "unk",
        enable_gpu: bool = False,
    ):
        """initializer

        Args:
            normalize(bool): text normalization flag e.g. unicode normalize
            sudachi_normalize(bool): text normalization which removes the conjungation
            lower     (bool): text lowerize flag (in japanese it doesn't effect)
            language(str): language type like "ja"
            enable_gpu(bool): allow to use gpu
        """
        super().__init__(normalize=normalize, lower=lower, language=language)
        self.vocab = vocab
        self.analyzer = Analyzer(
            model_path=None,
            sudachipy_mode=SUDACHIPY_DEFAULT_SPLIT_MODE,
            use_sentence_separator=None,
            hash_comment="print",
            output_format="mecab",
            require_gpu=enable_gpu,
        )
        self.analyzer.set_nlp()
        self.sudachi_normalize = sudachi_normalize

    def _mecab_token_to_keyword(self, token):
        """token to keyword

        Args:
            token: sudachipy's token

        Returns:
            str: token(normalized / unnormalized)
        """
        if self.sudachi_normalize:
            return token.normalized_form()
        else:
            return token.surface()

    def _analyze_mecab(self, sudachipy_tokens: List):
        """sudachipy's token to string words tuple

        Args:
            sudachipy_tokens(List): sudachipy's tokens

        Returns:
            Tuple(str): words list
        """
        return tuple(self._mecab_token_to_keyword(token) for token in sudachipy_tokens)

    def _analyze(self, line: str):
        """sentence line to splitted sentence line(words)
        Args:
            line(str): a sentence line
        Returns:
            words(Tuple(str)): words list
        """
        line = line.rstrip()
        if line == "":
            return ""
        doc = self.analyzer.nlp.tokenize(line)
        return self._analyze_mecab(doc)

    def tokenize(self, sentence: str):
        """tokenize a sentence
        Args:
            sentence(str): a sentence
        
        Retuens:
            tokens(Tuple[str]): tokens

        Example:
            >>> tokenizer.tokenize("おはようございます。おやすみなさい", True)
            ["おはよう", "ござい", "ます", "おやすみ", "なさい"]
            >>> tokenizer.tokenize("おはようございます。おやすみなさい", False)
            [["おはよう", "ござい", "ます"], ["おやすみ", "なさい"]]
        """
        sentence = self._normalize(sentence) if self.normalize else sentence
        return self._analyze(sentence)

    def tokenize_list(self, sentences: List[str]):
        """tokenize sentences
        
        Args:
            sentences(List[str]): sentences
        
        Retuens:
            tokens(List[Tuple[str]]): list of tokens
        
        Example:
            
            >>> tokenizer.tokenize(["おはようございます", "こんにちは"])
            [["おはよう", "ござい", "ます"], ["こんにちは"]]
        """
        return [self.tokenize(sentence) for sentence in sentences]

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

    def vocab_size(self):
        return len(self.vocab)


if __name__ == "__main__":
    import pprint

    tokenizer = SudachiTokenizer(language="ja")

    sentences = ["銀座でランチをご一緒しましょう。", "締切間に合いますか？", "トークナイザを作りました。"]
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

    tokenizer = SudachiTokenizer(vocab=vocab, language="ja")
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
    assert 10 == len(vocab)
