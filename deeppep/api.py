from fastapi import FastAPI
from .types import *
from .preprocessing import (
        DEFAULT_PREPROCESSING_CONFIG, 
        merge_configs,
        PreprocessingManager
        )
from .prediction import PREBUILT_CONFIG, PredictionManager

app = FastAPI()

@app.get("/config/preprocessing")
async def get_preprocessing_config():
    pre_config = DEFAULT_PREPROCESSING_CONFIG.copy()

    return pre_config

@app.get("/config/preprocessing/{model}")
async def get_model_preprocessing_config(model: str):
    model_config = PREBUILT_CONFIG[model]
    pre_config = DEFAULT_PREPROCESSING_CONFIG.copy()
    pre_config = merge_configs(pre_config, 
                               model_config.get("pre_config", {})
                               )

    return pre_config

@app.post("/predict/{model}", response_model=Prediction)
async def predict(model: str, input: PredictionInput):
    # Load Model
    model_config = PREBUILT_CONFIG[model]
    pred_man = PredictionManager(model_name=model,
                                 config_path=model_config["config_path"],
                                 weight_path=model_config["weight_path"])

    # Load Preprocessor
    pre_config = DEFAULT_PREPROCESSING_CONFIG.copy()
    pre_config = merge_configs(pre_config,
                               model_config.get("pre_config", {})
                               )
    if input.config is not None:
        pre_config = merge_configs(pre_config,
                                   input.config.dict()
                                   )
    prep_man = PreprocessingManager(**pre_config)

    # Run Pipeline
    enc_peptides = prep_man.preprocess(input.peptides.sequences)
    pred = pred_man.predict(enc_peptides).tolist()

    return {"values" : pred}

