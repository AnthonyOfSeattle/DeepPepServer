from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

###############
# Basic Types #
###############

class PeptideProperty(str, Enum):
    rt = "rt"
    charge = "charge"
    spectra = "spectra"
    mobility = "mobility"

class Action(str, Enum):
    predict = "predict"
    encode = "encode"

#################
# Request Model #
#################

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

##################
# Response Model #
##################

class Prediction(BaseModel):
    values : List[List[float]]

class InternalConfig(BaseModel):
    pattern       : str
    vocab         : dict
    max_vocab_dim : int
    seq_len       : int
    one_hot       : bool
