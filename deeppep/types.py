from typing import List, Optional
from pydantic import BaseModel

#################
# Request Model #
#################

class Config(BaseModel):
    pattern : Optional[str] = "[A-Zn][^A-Zn]*"
    vocab   : Optional[dict] = {}

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
    values: List[List[float]]
