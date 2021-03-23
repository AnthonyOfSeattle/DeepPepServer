from .manager import PredictionManager

PREBUILT_CONFIG = {
    "phospho_rt_gru_512" : {
        "pre_config"     : {"vocab" : {"S[80]": 24,
                                       "T[80]": 25,
                                       "Y[80]": 26},
                            "max_vocab_dim" : 26},
        "config_path"    : "deeppep/prediction/models/phospho_rt_gru_512.config.json",
        "weight_path"    : "deeppep/prediction/models/phospho_rt_gru_512.weights.h5",
        "property"       : "rt",
        "output_labels"  : ["rt"],
        "allow_encoding" : True,
        "public"         : True
        },
    "human_phosphopedia_rt" : {
        "pre_config"     : {"vocab" : {"S[80]": 24, 
                                       "T[80]": 25, 
                                       "Y[80]": 26},
                            "max_vocab_dim" : 26},
        "config_path"    : "deeppep/prediction/models/human_phosphopedia_rt.config.json",
        "weight_path"    : "deeppep/prediction/models/human_phosphopedia_rt.weights.h5",
        "property"       : "rt",
        "output_labels"  : ["rt"],
        "allow_encoding" : False,
        "public"         : True
        },
}

PREBUILT_CONFIG["phospho_rt"] = PREBUILT_CONFIG["phospho_rt_gru_512"]

