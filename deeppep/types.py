from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

####################
# Global Variables #
####################

DEFAULT_VOCAB = {
    "X": 0,
    "n[42]": 1,
    "A": 2,
    "C": 3,
    "C[57]": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "P": 14,
    "Q": 15,
    "R": 16,
    "S": 17,
    "T": 18,
    "U": 19,
    "V": 20,
    "W": 21,
    "Y": 22,
    "M[16]": 23,
}

############
# Internal #
############

class PeptideProperty(str, Enum):
    rt = "rt"
    charge = "charge"
    spectra = "spectra"
    mobility = "mobility"
    other = "other"

class Action(str, Enum):
    predict = "predict"
    encode = "encode"

class PreprocessingConfig(BaseModel):
    pattern       : Optional[str] = "[A-Zn][^A-Zn]*"
    vocab         : Optional[dict] = DEFAULT_VOCAB
    max_vocab_dim : Optional[int] = 23
    seq_len       : Optional[int] = 50
    one_hot       : Optional[bool] = False

class ModelSpec(BaseModel):
    model_name     : str
    config_path    : Optional[str] = ""
    weight_path    : Optional[str] = ""
    pre_config     : Optional[PreprocessingConfig] = PreprocessingConfig()
    property       : Optional[str] = "other"
    output_labels  : Optional[List[str]] = None
    allow_encoding : Optional[bool] = False
    public         : Optional[bool] = False

############
# Requests #
############

class Config(BaseModel):
    pattern : Optional[str] = "[A-Zn][^A-Zn]*"
    vocab   : Optional[dict] = {}

class UserConfig(BaseModel):
    pattern : Optional[str] = None
    vocab   : Optional[dict] = None

class Peptide(BaseModel):
    sequence : str
    charge   : Optional[int] = None 

class ModelInput(BaseModel):
    peptides : List[Peptide]
    config   : Optional[UserConfig] = None

class PeptideSet(BaseModel):
    sequences : List[str]
    charges   : Optional[List[int]] = []

class PredictionInput(BaseModel):
    config  : Optional[Config] = None
    peptides: PeptideSet

#############
# Responses #
#############

class Prediction(BaseModel):
    values : List[List[float]]

########
# Util #
########

def merge_configs(left, right):
    # Copy to maintain read only
    left_dict = left.dict()
    right_dict = right.dict()

    # Pop out vocab dict and copy
    merged_vocab = left_dict.pop("vocab").copy()
    merged_vocab.update(right_dict.pop("vocab"))

    # Create final merged config
    merged = left_dict
    merged.update(right_dict)
    merged["vocab"] = merged_vocab

    return PreprocessingConfig(**merged)
