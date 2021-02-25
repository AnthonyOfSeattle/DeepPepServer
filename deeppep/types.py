from typing import List, Optional
from pydantic import BaseModel

#########################
# Preprocressing Config #
#########################

class EncoderConfig(BaseModel):
    pattern : Optional[str] = "[A-Z][^A-Z]*"
    vocab   : Optional[dict] = {}

##################
# Request Models #
##################

class PeptideSet(BaseModel):
    peptides: List[str]

class ExtendedPeptideSet(BaseModel):
    peptides: List[str]
    charges : List[int]

###################
# Response Models #
###################

class Prediction1D(BaseModel):
    model: str
    values: List[float]

class Prediction2D(BaseModel):
    model: str
    values: List[List[float]]
