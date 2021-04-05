from fastapi import FastAPI, Path, Query, Body
from .manager import PipelineManager
from .types import *

app = FastAPI(
        title="Deep Peptide Server",
        description="A REST API providing uniform access to"
                    " deep models of peptide properties",
        version="0.1.0",
        openapi_tags=[
            {"name": "models",
             "description": "Operations to utilize models on sets of peptides"
                            " and download models locally."}
        ]   
        )

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
        response_model=PreprocessingConfig)
async def get_model_preprocessor_config(
        model_name: str = Path(
        ..., title="Model Name",
        description="Name of model to download."
        ),
        config: Optional[UserConfig] = Body(
            None, title="User Supplied Config",
            description="Configuration parameters to patch over defaults",
            example={"pattern" : "[A-Zn][^A-Zn]*",
                     "vocab"   : {"M<ox>" : 23}}
            )
        ):
    pipeline = PipelineManager(model_name, config)
    return pipeline.pre_config

@app.post("/models/{model_name}/{action}",
          tags=["models"])#, 
          #response_model=List[dict])
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
    pipeline = PipelineManager(model_name, model_input.config)
    output = pipeline.run(model_input.peptides, action)
    return output

