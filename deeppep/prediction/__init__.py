from .manager import PredictionManager

PREBUILT_CONFIG = {
    "human_phosphopedia_rt" : {
        "pre_config" : {"vocab" : {"S[80]": 24, 
                                   "T[80]": 25, 
                                   "Y[80]": 26},
                        "max_vocab_dim" : 26},
        "config_path" : "deeppep/prediction/models/phospho_rt_config.json",
        "weight_path" : "deeppep/prediction/models/phospho_rt_weights.h5"
        },
}

PREBUILT_CONFIG["aliases"] = {"phospho_rt" : PREBUILT_CONFIG["human_phosphopedia_rt"]}

