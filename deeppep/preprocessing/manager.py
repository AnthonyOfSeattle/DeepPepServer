import re
from itertools import chain
from fastapi import HTTPException
from .encoder import SequenceEncoder


GLOBAL_VOCAB = {"X": 0,  "A": 1,  "C": 2,  
                "D": 3,  "E": 4,  "F": 5,  
                "G": 6,  "H": 7,  "I": 8,  
                "K": 9,  "L": 10, "M": 11, 
                "N": 12, "P": 13, "Q": 14, 
                "R": 15, "S": 16, "T": 17, 
                "V": 18, "W": 19, "Y": 20}


class PreprocessingManager:
    def __init__(self, pattern, vocab=None, max_vocab_dim=20, **kwargs):
        self.pattern = pattern
        
        self.max_vocab_dim = max_vocab_dim
        self.vocab = GLOBAL_VOCAB.copy()
        if vocab is not None:
            self.vocab.update(vocab)
        self._check_vocab_dim()
        
        self.encoder = SequenceEncoder(pattern, self.vocab, **kwargs)

    def _vocab_dim_message(self, cur_vocab_dim, vocab_dim):
        message = " ".join([
            "PREPROCESSING ERROR:",
            "Vocabulary is of size {},",
            "and the current model supports size {}.",
            "Please use a different model",
            "or mask using X."
            ]).format(cur_vocab_dim, vocab_dim)

        return message

    def _check_vocab_dim(self):
        cur_vocab_dim = max(self.vocab.values())
        if cur_vocab_dim > self.max_vocab_dim:
            raise HTTPException(status_code = 400,
                                detail = self._vocab_dim_message(cur_vocab_dim,
                                                                 self.max_vocab_dim)
                               )

    def _unknown_tokens_message(self, tokens):
        token_string = ", ".join(tokens)
        message = " ".join([
            "PREPROCESSING ERROR:",
            "Encountered unknown tokens -- {} --",
            "using the pattern '{}'.", 
            "Please include custom vocabulary."
            ]).format(token_string, self.pattern)

        return message

    def _check_consistency(self, sequences):
        oov_set = set(chain.from_iterable(
            [re.findall(self.pattern, seq) for seq in sequences]
            ))
        oov_set.difference_update(self.vocab.keys())

        if oov_set:
            raise HTTPException(status_code = 400,
                                detail = self._unknown_tokens_message(oov_set)
                                )

    def preprocess(self, input):
        self._check_consistency(input)
        output = self.encoder.transform(input)

        return output
    
