import re
import warnings
import numpy as np
from itertools import chain
from sklearn.base import TransformerMixin


class SequenceEncoder(TransformerMixin):
    """Transformer to parse and encode biological sequences.

    This class is a custom sklearn Transformer which is designed
    to flexibly parse biological sequences using a regular expression
    and encode them as either padded integer vectors or padded
    one hot encoded matrices. The padding label is fixed at 0.

    """
    def __init__(self,
                 pattern="\w",
                 vocab=None,
                 seq_len=0,
                 one_hot=False,
                 oov_warn=True):
        """Create an encoder class with optional fixed parameters.

        The most important parameter here is the regex `pattern`, which must be
        tailored to the given dataset. The optional `vocab` parameter can be
        used to pass a premade dictionary of token to integer correspondences.
        These will not be overwritten, but new tokens can still be learned.
        In the case that a predefined length is necessary, it can be determined
        by the `seq_len` variable. By default, the class will return data with
        an integer encoding, but a one hot encoding can be returned with `one_hot=True`.
        Finally, the class will spit out warnings when a token is not found in the vocabulary.
        In these cases, the position will be treated as a blank.

        Args:
            pattern (str): Regular expression for tokenizing sequences. Defaults to \w.
            vocab (dict): Pre-built token to integer correspondences. Defaults to None.
            seq_len (int): Fixed sequence length for final encodings. Defaults to 0.
            one_hot (bool): Encoding toggle. False for integer, True for one hot. Defaults to False.
            oov_warn (bool): Warning toggle. Defaults to True.

        """
        self.vocab = {} if vocab is None else vocab
        self.regex = re.compile(pattern)
        self.seq_len = seq_len
        self.one_hot = one_hot
        self.oov_warn = oov_warn

    # START: Fit functions

    def _unique_tokens(self, input):
        """Find unique tokens in the input using the user's regex query.

        Args:
            input (List[str]): Sequences to scan for tokens.

        Returns:
            List[str]: All tokens found at least once in input.

        """
        unique_tokens = set(chain.from_iterable(
            [self.regex.findall(seq) for seq in input]
        ))
        unique_tokens = sorted(unique_tokens)

        return unique_tokens

    def _tokens_to_vocab(self, input):
        """Covert a sequence of tokens to new vocab entries.

        Tokens will start where the current vocab leaves off and only tokens
        which are not already in the vocab will be added.

        Args:
            input (List[str]): A list of tokens to add to the vocabulary.

        Returns:
            dict: New vocabulary items.

        """
        new_vocab = {}
        index_start = max(self.vocab.values()) + 1 if self.vocab else 1
        for ind, tok in enumerate(input, index_start):
            if tok not in self.vocab:
                new_vocab[tok] = ind

        return new_vocab

    def fit(self, X, y=None, **kwargs):
        """Build vocab using the inputed sequences.

        Sequences inputed in X are iterated through and converted to tokens
        using the user specified regex. Any tokens not present in the vocab
        are added.

        Args:
            X (List[str]): Input sequences to use to build vocabulary.
            y: Not used. Present for consistency.
            **kwargs: Not used. Present for consistency.

        Returns:
            SequenceEncoder: Return self for chaining.

        """
        X = np.atleast_1d(X)
        token_count = self._unique_tokens(X)
        self.vocab.update(self._tokens_to_vocab(token_count))

        return self

    # START: Transform functions

    def _warn_oov(self):
        """Warn if token is not found in vocabulary and self.oov_warn==True."""
        if self.oov_warn:
            warnings.warn("Token not found in vocabulary", RuntimeWarning)

    def _get_seq_len(self, input):
        """Get length of final encoding sequences.

        The user specified length will be returned if available, otherwise
        the length of the longest sequence will be used.

        Args:
            input (List[str]): Sequences to iterate through.

        Returns:
            int: Length of longest sequence or user specified length if available.

        """
        if self.seq_len > 0:
            seq_len = self.seq_len
        else:
            seq_len = max(map(
                lambda seq: len(self.regex.findall(seq)), input
                ))

        return seq_len

    def _create_encoding(self, input):
        """Covert a list of strings into an int32 encoded sequence.

        Sequences are iterated through and converted into an NxM matrix of int32. 
        N is determined by the first dimension of X and M is determined by the 
        results of self._get_seq_len. The user specified regex string is used 
        to iterate through the sequences until M tokens are analyzed. 
        Sequences shorter than M are extended by padding with 0.

        Args:
            input (List[str]): Tokenized sequences.

        Returns:
            ndarray(dtype=int32): Integer encoding of input sequences.

        """
        seq_len = self._get_seq_len(input)
        out = np.zeros(shape=(input.shape[0], seq_len),
                       dtype=np.int32)

        for seq_ind, seq in enumerate(input):
            for match_ind, match in enumerate(self.regex.findall(seq)):
                if match_ind == seq_len:
                    break

                try:
                   out[seq_ind, match_ind] = self.vocab[match]
                except KeyError:
                    self._warn_oov()

        return out

    def _encoding_to_one_hot(self, input):
        """Create a one hot encoding from a pre-made integer encoding.

        An integer encoding matrix of shape NxM is converted to a one hot
        matrix of shape NxMxV. Values in the integer encoding are decreased
        by 1 and padding vectors are left entirely as 0.

        Args:
            input (ndarray(dtype=int32)):

        Returns:
            ndarray(dtype=float32):

        """
        vocab_size = max(self.vocab.values())
        out = np.zeros(shape=(input.shape[0],
                              input.shape[1],
                              vocab_size + 1),
                        dtype=np.float32)
        for row_ind, row in enumerate(input):
            out[row_ind][np.arange(row.shape[0]), row] = 1.

        out = out[:, :, 1:]

        return out

    def transform(self, X, **kwargs):
        """Transform a list of sequences into user specified encodings.

        Args:
            X (List[str]): Input sequences to transform.
            **kwargs: Not used. Present for consistency.

        Returns:
            ndarray: Output encoding, type determined by `self.one_hot`.

        """
        X = np.atleast_1d(X)
        out = self._create_encoding(X)
        if self.one_hot:
            out = self._encoding_to_one_hot(out)

        return out

