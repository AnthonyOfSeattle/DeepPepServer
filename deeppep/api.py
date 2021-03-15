from fastapi import FastAPI, Path, Query, Body
from .types import *
from .preprocessing import (
        DEFAULT_PREPROCESSING_CONFIG, 
        merge_configs,
        PreprocessingManager
        )
from .prediction import PREBUILT_CONFIG, PredictionManager

app = FastAPI(
        title="Deep Peptide Sever",
        description="A REST API providing uniform access to"
                    " deep models of peptide properties",
        version="0.1.0",
        openapi_tags=[
            {"name": "models",
             "description": "Operations to utilize models on sets of peptides"
                            " and download models locally."}
        ]   
        )

@app.get("/config/preprocessing", tags=["deprecated"])
async def get_preprocessing_config():
    pre_config = DEFAULT_PREPROCESSING_CONFIG.copy()

    return pre_config

@app.get("/config/preprocessing/{model}", tags=["deprecated"])
async def get_model_preprocessing_config(model: str):
    model_config = PREBUILT_CONFIG[model]
    pre_config = DEFAULT_PREPROCESSING_CONFIG.copy()
    pre_config = merge_configs(pre_config, 
                               model_config.get("pre_config", {})
                               )

    return pre_config

@app.post("/predict/{model}", response_model=Prediction, tags=["deprecated"])
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

#################
# New endpoints #
#################

@app.options("/models", 
             tags=["models"])
async def get_prediction_api_options(
    peptide_property: Optional[PeptideProperty] = Query(
        None, title="Peptide Property",
        description="A peptide property can be specified to restrict"
                    " options to models that predict that property."
        )
    ): 
    return {}

@app.get("/models/{model_name}",
         tags=["models"])
async def get_model(
    model_name: str = Path(
        ..., title="Model Name",
        description="Name of model to download."
        )
    ):
    return {}

@app.get("/models/{model_name}/preprocessor/config", 
        tags=["models"],
        response_model=InternalConfig)
async def get_model_preprocessor_config(
        config: Optional[UserConfig] = Body(
            None, title="User Supplied Config",
            description="Configuration parameters to patch over defaults",
            example={"pattern" : "[A-Zn][^A-Zn]*",
                     "vocab"   : {"M<ox>" : 23}}
            )
        ):
    return {}

@app.post("/models/{model_name}/{action}",
          tags=["models"], 
          response_model=List[dict])
async def post_peptides_to_model(
    model_name: str = Path(
        ..., title="Model Name",
        description="Name of model to perform predictions with."
        ),
    action: Action = Path(
        ..., title="Action to Perform",
        description="Specify whether to return predictions or encodings of sequences"
        ),
    model_input: ModelInput = Body(
        ..., title="Input For Models",
        example={
            "peptides": [
                {"sequence" : "PEPTIDEK", "charge" : 0},
            ],
            "config": {"pattern" : "[A-Zn][^A-Zn]*",
                       "vocab"   : {"M<ox>" : 23}}
            }
        )
    ):
    return {}

