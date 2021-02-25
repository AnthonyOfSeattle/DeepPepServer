from fastapi import FastAPI
from .types import *
from .preprocessing import PreprocessingManager

app = FastAPI()

@app.put("/predict/rt/{model}", response_model=Prediction1D)
async def predict_properties(model: str, enc_conf: EncoderConfig, input: PeptideSet):
    # Preprocess data
    pm = PreprocessingManager(**enc_conf.__dict__)
    enc_peptides = pm.preprocess(input.peptides)
    print(enc_peptides)
    return {"model"  : model,
            "values" : [1,2,3,4]}
