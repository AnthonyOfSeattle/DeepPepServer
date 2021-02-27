from fastapi import FastAPI
from .types import *
from .preprocessing import PreprocessingManager
from .prediction import PREBUILT_CONFIG, PredictionManager

app = FastAPI()

@app.get("/config/encoder")
async def get_config_encoder(enc_conf: EncoderConfig):
    config = {"pattern"  : "[A-Zn][^A-Zn]*"}
    config.update(enc_conf.__dict__)

    return config

@app.post("/predict/{model}", response_model=Prediction)
async def predict(model: str, enc_conf: EncoderConfig, input: PeptideSet):
    # Preprocess data
    model_config = PREBUILT_CONFIG["__default__"]
    model_config.update(PREBUILT_CONFIG[model])
    pred_man = PredictionManager(model_name=model,
                                 config_path=model_config["config_path"],
                                 weight_path=model_config["weight_path"])

    enc_conf = enc_conf.__dict__
    enc_conf["max_vocab_dim"] = model_config["max_vocab_dim"]
    enc_conf["seq_len"] = model_config["seq_len"]
    enc_conf["one_hot"] = model_config["one_hot"]
    prep_man = PreprocessingManager(**enc_conf)

    enc_peptides = prep_man.preprocess(input.peptides)
    pred = pred_man.predict(enc_peptides)

    return {"model"  : model,
            "values" : pred.tolist()}
