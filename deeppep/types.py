from typing import List, Optional
from pydantic import BaseModel

#########################
# Preprocressing Config #
#########################

class EncoderConfig(BaseModel):
    pattern : Optional[str] = "[A-Zn][^A-Zn]*"
    vocab   : Optional[dict] = {}

#################
# Request Model #
#################

class PeptideSet(BaseModel):
    peptides: List[str]
    charges : Optional[List[int]] = []

##################
# Response Model #
##################

class Prediction(BaseModel):
    model: str
    values: List[List[float]]
